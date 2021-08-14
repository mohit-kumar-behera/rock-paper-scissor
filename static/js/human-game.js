/*
r - rock
p - paper
s - scissor

pA - You
pB - Opponent
*/
const keyChoices = ['r','p','s'];
const imageChoices = ['rock','paper','scissor'];

const d = document;
const pA_icon_elem = d.getElementsByClassName("pA-icon")[0];
const pB_icon_elem = d.getElementsByClassName("pB-icon")[0];	
const pA_score_elem = d.getElementsByClassName("pA-score")[0];
const pB_score_elem = d.getElementsByClassName("pB-score")[0];
const game_message_elem = d.getElementsByClassName("game-message")[0];
const gamePoint = game_message_elem.getAttribute('data-points');

var pA_score = 0;
var pB_score = 0; 
var canType = true;


function setImage(elem, imgPath) { elem.setAttribute('src', imgPath); }

function createImgPath(key, elem) {
    let imgPath = '';
    if (key === 0)
        imgPath = "/static/media/rock.png";
    else if (key === 1)
        imgPath = "/static/media/paper.png";
    else
        imgPath = "/static/media/scissor.png";
    
    setImage(elem, imgPath)
}

d.onkeyup = function(event) {
    if(canType) {
        if(pA_score == gamePoint || pB_score == gamePoint) { return false;/*Game is over and winnner is decided*/}
        else {
            //Game is still ON
            keyPressed = event.key.toLowerCase();
            if(keyChoices.includes(keyPressed)) {
                //keypressed is r,p,s
                keyPosition = keyChoices.indexOf(keyPressed);
                createImgPath(keyPosition, pA_icon_elem);
                checkResult();
                var waitForOpponent = setInterval(checkResult,3000);
                function checkResult() {
                    $.ajax({
                        type:'GET',
                        url:"/play/human-compare/",
                        data:{
                            'userChose':imageChoices[keyPosition]
                        },
                        success:function(json) {
                            if(json.opponentSelected) {
                                //Opponent has selected his choice, User can go for next choice
                                clearInterval(waitForOpponent);
                                let pBChoice = json.playerB_Choice;
                                createImgPath(pBChoice, pB_icon_elem);
                                let pA_Win = json.pA_Win
                                if(pA_Win != "tie") {
                                    (pA_Win)?game_message_elem.innerHTML="You Win 1 Point":game_message_elem.innerHTML="You Loose";
                                    (pA_Win)?pA_score+=1:pB_score+=1;
                                }else { //Its a tie
                                    game_message_elem.innerHTML="It's a tie";
                                }
                                pA_score_elem.innerHTML = pA_score;
                                pB_score_elem.innerHTML = pB_score;
                                //Game start again and now he can select his next choice
                                setTimeout(function(){
                                    resetChoice();
                                    if (pA_score == gamePoint || pB_score == gamePoint) {
                                        (pA_score == gamePoint)?userWins():opponentWins();
                                        $("#result-message-modal").modal({
                                            show:true,
                                            backdrop:'static',
                                            keyboard:false
                                        });
                                        canType = false;
                                        game_message_elem.innerHTML = "Game Over";
                                        setTimeout(function(){
                                            return location.reload();
                                        },10000)
                                    }else {
                                        canType = true;
                                        game_message_elem.innerHTML = "Next Turn";
                                    }
                                },1500);									
                            }else{
                                //Opponent has not selected yet, User cant go for next choice
                                canType = false;
                            }
                        }
                    });
                }
            }
            else {
                //keypressed is not r,p,s
                alert("You have only three Choices - r,p,s");
            }
        }
    } else { return false; }   
}

function resetChoice() {
    $.ajax({
        type:"GET",
        url:"/play/reset-choice/",
        data:{
            'reset_choice':true,
        },
        success:function(json) {
            if(json.successfullReset) {
                pA_icon_elem.setAttribute("src","https://i.pinimg.com/originals/65/ba/48/65ba488626025cff82f091336fbf94bb.gif");
                pB_icon_elem.setAttribute("src","https://i.pinimg.com/originals/65/ba/48/65ba488626025cff82f091336fbf94bb.gif");
            }
        }
    });
}	

function userWins() {
    $(".result-tag").html("Congratulation 😊😎");
    $(".result-message").html("You won the game against {{ playerB }}.");
}	
function opponentWins() {
    $(".result-tag").html("Oops 😥😥");
    $(".result-message").html("You lost the game against {{ playerB }}.");
}