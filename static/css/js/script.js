// ============================
// PAGE LOADED
// ============================

document.addEventListener("DOMContentLoaded", function () {


    console.log(
        "AI Movie Recommendation System Loaded"
    );



    // ============================
    // LOAD THEME
    // ============================


    const savedTheme =
        localStorage.getItem("theme");


    const themeBtn =
        document.getElementById("themeBtn");



    if(savedTheme === "light"){

        document.body.classList.add(
            "light-mode"
        );

    }



    if(themeBtn){


        themeBtn.innerHTML =
            document.body.classList.contains("light-mode")
            ? "☀️"
            : "🌙";



        themeBtn.addEventListener(
            "click",
            function(){



                document.body.classList.toggle(
                    "light-mode"
                );



                if(
                document.body.classList.contains("light-mode")
                ){


                    localStorage.setItem(
                        "theme",
                        "light"
                    );


                    themeBtn.innerHTML="☀️";


                }

                else{


                    localStorage.setItem(
                        "theme",
                        "dark"
                    );


                    themeBtn.innerHTML="🌙";


                }


            }
        );


    }






    // ============================
    // AUTO CLOSE ALERT
    // ============================


    setTimeout(()=>{


        document
        .querySelectorAll(".alert")
        .forEach(alert=>{


            alert.classList.remove(
                "show"
            );


            setTimeout(()=>{

                alert.remove();

            },300);


        });


    },3000);






});







// ============================
// SEARCH VALIDATION
// ============================


const form =
document.querySelector("form");



if(form){


form.addEventListener(
"submit",
function(e){


const movie =
document.querySelector(
'input[name="movie"]'
);



if(movie && movie.value.trim()===""){


alert(
"Please enter a movie name."
);


e.preventDefault();


}



});


}








// ============================
// LOADING BUTTON
// ============================


function showLoading(){


const btnText =
document.getElementById(
"btnText"
);


const loader =
document.getElementById(
"loader"
);



if(btnText && loader){


btnText.style.display="none";


loader.style.display="inline";


}



}







// ============================
// BUTTON HOVER EFFECT
// ============================


document
.querySelectorAll(".btn")
.forEach(btn=>{


btn.addEventListener(
"mouseenter",
()=>{


btn.style.transform =
"scale(1.05)";


});



btn.addEventListener(
"mouseleave",
()=>{


btn.style.transform =
"scale(1)";


});


});







// ============================
// CARD SCROLL ANIMATION
// ============================


window.addEventListener(
"scroll",
function(){



const cards =
document.querySelectorAll(
".card,.movie-card,.movie-glass-card"
);



cards.forEach(card=>{


const position =
card.getBoundingClientRect().top;



if(
position <
window.innerHeight-80
){


card.style.opacity="1";


card.style.transform =
"translateY(0)";


}



});



});