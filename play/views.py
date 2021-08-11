from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.urls import reverse
from .passwordGenerator import passwordGenerator as PG
from .models import Room
import random
import time
import math

# COMPUTER
def default_redirect_computer(request):
	return HttpResponseRedirect(reverse("play:computer"))

def redirect_computer(request,unknown_player):
	return HttpResponseRedirect(reverse("play:computer"))

def play_with_computer(request):
	return render(request,"play/computer-index.html",{})

def start_game(request,points):
	context = {}
	if points not in [3,5,10]:
		points = 5 #default points
		context['message'] = "Points entered are not valid. Default is a 5 pointer game. You can go back and change the points."
	context['instruction'] = "Press Key <u><b>&quot;R&quot;</b> for Rock</u>, <u><b>&quot;P&quot;</b> for Paper</u>, <u><b>&quot;S&quot;</b> for Scissor</u>."
	context['points'] = points
	return render(request,"play/computer-start.html",context)

def who_win(request):
	rps_choice = ['rock','paper','scissor']
	if request.GET:
		data = {}
		userChoice = request.GET.get('keyPressed')
		computerChoice = random.randint(0,2)
		userChoiceIndex = rps_choice.index(userChoice)
		if userChoiceIndex == 0 and computerChoice == 1:
			data['userWin'] = False
		elif userChoiceIndex == 0 and computerChoice == 2:
			data['userWin'] = True
		elif computerChoice == 0 and userChoiceIndex == 2:
			data['userWin'] = False
		elif userChoiceIndex > computerChoice:
			data['userWin'] = True
		elif userChoiceIndex < computerChoice:
			data['userWin'] = False
		elif computerChoice == userChoiceIndex:
			data['userWin'] = "Tie"
		data['computerChoice'] = computerChoice

		return JsonResponse(data)


# HUMAN
def play_with_human(request):
	context = {}
	unique_key = random.randint(1111,9999) # 4 digit random number
	password = PG.generateID(unique_key=unique_key)
	context['ID'] = password
	if request.POST:
		room_id = request.POST.get("unique-id")
		game_points = request.POST.get("points")
		player_name = request.POST.get("name")

		try:
			roomIdExists = Room.objects.filter(u_id=room_id)
		except:
			pass
		else:
			request.session['roomID'] = room_id
			request.session['playerName'] = player_name
			if len(roomIdExists) > 1:
				#More than 1 room with same ID cannot be created 
				del request.session['roomID']
				del request.session['playerName']
				context['message'] = "This Rooom ID already Exists. Get some new ID"
			elif len(roomIdExists) == 1:
				#Room already exists, Just player is need to be added
				'''
				NOTE: This room is already created 
					  Room strength is 2, One player is already added while creating the room
					  Only one player can be added now
				'''
				getRoom = Room.objects.get(u_id=room_id)
				getPlayersOfThisRoom = getRoom.player_set.all()
				if len(getPlayersOfThisRoom) == 1:
					# second player can be added
					setSecondPlayer = getRoom.player_set.create(player_name=player_name,points_decided=game_points,creater=False,rps_choice="")
					return HttpResponseRedirect(reverse("play:waiting-room"))
				else:
					#Room is full, New player cannot be added
					del request.session['roomID']
					del request.session['playerName']
					context['message'] = "This Room is already filled up."

			else:
				#Room doesnot exists, First create Room then add player  
				createRoom = Room.objects.create(u_id=room_id)
				getCreatedRoom = Room.objects.get(u_id=room_id)
				setFirstPlayer = getCreatedRoom.player_set.create(player_name=player_name,points_decided=game_points,creater=True,rps_choice="")
				#NOTE: This player created the room so he is the first player
				return HttpResponseRedirect(reverse("play:waiting-room"))
	return render(request,"play/human-index.html",context)


def waiting_room(request):
	return render(request,'play/human-start.html')

def waiting_for_opponent(request):
	try:
		room_id = request.session['roomID']
		room = Room.objects.get(u_id=room_id)
	except:
		return HttpResponseRedirect(reverse("play:human"))
	else:
		jsonData = {'playersJoined':False}
		players = room.player_set.all()
		if len(players) == 2:
			jsonData['playersJoined'] = True
			return JsonResponse(jsonData)
		return JsonResponse(jsonData)


def human_play(request):
	try:
		room_id = request.session['roomID']
		player_name = request.session['playerName']
		room = Room.objects.get(u_id=room_id)
	except:
		return HttpResponseRedirect(reverse("play:human"))
	else:
		context = {}
		context['instruction'] = "<p>Press Key <u><b>&quot;R&quot;</b> for Rock</u>, <u><b>&quot;P&quot;</b> for Paper</u>, <u><b>&quot;S&quot;</b> for Scissor</u></p><br><p><b>After choosing your choice wait for the next player to select their choice.</b></p>"

		players = room.player_set.all() #Query Set for Both the players of the room
		player_1 = room.player_set.first() #Query set for player 1 as per the database, he is the creater
		player_2 = room.player_set.last() #Query set for player 2 as per the database
		p1_points = player_1.points_decided
		p2_points = player_2.points_decided
		game_points = math.floor((p1_points+p2_points)/2)

		playerA = player_name # (You) this is the session Player
		for player in players:
			if player.player_name != playerA:
				playerB = player.player_name #opponent
		
		context.update({"playerA":playerA,"playerB":playerB,"gamePoints":game_points})	
		return render(request,"play/human-play.html",context)

def human_compare(request):
	try:
		room_id = request.session['roomID']
		player_name = request.session['playerName']
	except:
		pass
	else:
		rps_choice = ['rock','paper','scissor']
		playerA = player_name # (you) player
		data = {}
		room = Room.objects.get(u_id=room_id)
		players = room.player_set.all()
		for player in players:
			if player.player_name != playerA:
				playerB = player.player_name #opponent
		playerA_query = room.player_set.get(player_name=playerA)
		playerB_query = room.player_set.get(player_name=playerB)

		userChoice = request.GET.get("userChose")
		playerA_query.rps_choice = userChoice
		playerA_query.save()

		if playerB_query.rps_choice == None or playerB_query.rps_choice == "":
			data['opponentSelected'] = False
			return JsonResponse(data)
		else:
			pA_rps = playerA_query.rps_choice
			pB_rps = playerB_query.rps_choice
			pA_rpsIndex = rps_choice.index(pA_rps)
			pB_rpsIndex = rps_choice.index(pB_rps)
			data['playerB_Choice'] = pB_rpsIndex
			if pA_rpsIndex == 0 and pB_rpsIndex == 1: #rock and paper
				data['pA_Win'] = False
			elif pA_rpsIndex == 0 and pB_rpsIndex == 2: #rock and scissor
				data['pA_Win'] = True
			elif pB_rpsIndex == 0 and pA_rpsIndex == 2: #rock and scissor
				data['pA_Win'] = False
			elif pA_rpsIndex > pB_rpsIndex:
				data['pA_Win'] = True
			elif pA_rpsIndex < pB_rpsIndex:
				data['pA_Win'] = False
			elif pA_rpsIndex == pB_rpsIndex:
				data['pA_Win'] = "tie"
			time.sleep(1)
			data['opponentSelected'] = True
			return JsonResponse(data)


def reset_choice(request):
	room_id = request.session['roomID']
	playerName = request.session['playerName']
	playerA = playerName
	room = Room.objects.get(u_id=room_id)
	players = room.player_set.all()
	for player in players:
		if player.player_name != playerA:
			playerB = player.player_name 
	playerA_query = room.player_set.get(player_name=playerA)
	playerB_query = room.player_set.get(player_name=playerB)
	playerA_query.rps_choice = ""
	playerA_query.save()
	playerB_query.rps_choice = ""
	playerB_query.save()
	data = {'successfullReset':True}
	return JsonResponse(data)

def go_home(request):
	try:
		room_id = request.session['roomID']
		room = Room.objects.get(u_id=room_id)
	except:
		return HttpResponseRedirect(reverse("home:home"))
	else:
		room.delete()
		return HttpResponseRedirect(reverse("home:home"))