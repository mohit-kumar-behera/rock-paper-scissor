/*
    r - Rock (0)
    p - Paper (1)
    s - Scissor (2)
*/
const d = document;
const user_icon_elem = d.getElementsByClassName("user-icon")[0];
const computer_icon_elem = d.getElementsByClassName("computer-icon")[0];
const game_message_elem = d.getElementsByClassName("game-message")[0];
const human_score_elem = d.getElementsByClassName("human-score")[0];
const computer_score_elem = d.getElementsByClassName("computer-score")[0];
const gamePoint = game_message_elem.getAttribute('data-id');

const keyChoices = ['r','p','s'];
const imageChoices = ['rock','paper','scissor'];

var user_score = 0;
var computer_score = 0; 

function userWins() {
    $(".result-tag").html("Congratulation 😊😎");
    $(".result-message").html("You won the game against Computer.");
}
function computerWins(){
    $(".result-tag").html("Oops 😥😥");
    $(".result-message").html("You lost the game against Computer.");		
}

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

document.onkeyup = function(event) {

    if(user_score == gamePoint ||  computer_score == gamePoint) {
        location.reload();			
        return false;
    }
    else {
        keyPressed = event.key.toLowerCase();			
        if(keyChoices.includes(keyPressed)) {
            //Key is present in choices
            keyPosition = keyChoices.indexOf(keyPressed);
            createImgPath(keyPosition, user_icon_elem);
            $.ajax({
                type:'GET',
                url:"/play/who-win/",
                data:{
                    'keyPressed':imageChoices[keyPosition]
                },
                success:function(json){
                    //success
                    computerChoice = json.computerChoice;
                    createImgPath(computerChoice, computer_icon_elem);
                    userWin = json.userWin;
                    if(userWin != "Tie") {
                        (userWin)?game_message_elem.innerHTML="You win 1 point":game_message_elem.innerHTML="You loose 1 point";
                        (userWin)?user_score += 1:computer_score += 1;
                    }else {
                        game_message_elem.innerHTML="This was a tie";
                    }
                    human_score_elem.innerHTML = user_score;
                    computer_score_elem.innerHTML = computer_score;

                    if(user_score == gamePoint || computer_score == gamePoint) {
                        //game is complete and final result is decided
                        (user_score==gamePoint)?userWins():computerWins();
                        $("#result-message-modal").modal("show");
                    }

                }
            })
        }
        else {
            alert("You have only three Choices - r,p,s");
        }
    }
}