from django.urls import path
from . import views

app_name = "play"

urlpatterns = [
	path('',views.default_redirect_computer,name="default_play"),
    path('computer/',views.play_with_computer,name="computer"),
    path('human/',views.play_with_human,name="human"),
    path('computer/<int:points>/',views.start_game,name="start-game"),
    path('who-win/',views.who_win,name="who-win"),
    path('waiting-room/',views.waiting_room,name="waiting-room"),
    path('wait-for-opponent/',views.waiting_for_opponent,name="wait-for-opponent"),
    path("human/game-start/",views.human_play,name="human-game-start"),
    path("human-compare/",views.human_compare,name="human-compare"),
    path("reset-choice/",views.reset_choice,name="reset-choice"),
    path("go-home/",views.go_home,name="go-home")
]
