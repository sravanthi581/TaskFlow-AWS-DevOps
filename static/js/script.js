// ============================
// TASKFLOW PRO
// ============================

document.addEventListener("DOMContentLoaded", () => {

    animateCards();

    animateCounters();

    darkMode();

    enableTooltips();

    smoothButtons();

});

// ============================
// CARD ANIMATION
// ============================

function animateCards(){

    const cards=document.querySelectorAll(".card");

    cards.forEach((card,index)=>{

        card.style.opacity=0;

        card.style.transform="translateY(25px)";

        setTimeout(()=>{

            card.style.transition="0.6s";

            card.style.opacity=1;

            card.style.transform="translateY(0px)";

        },index*120);

    });

}

// ============================
// COUNTER ANIMATION
// ============================

function animateCounters(){

    const counters=document.querySelectorAll(".dashboard-card h2");

    counters.forEach(counter=>{

        const target=parseInt(counter.innerText);

        let current=0;

        const increment=Math.max(1,Math.ceil(target/40));

        const timer=setInterval(()=>{

            current+=increment;

            if(current>=target){

                counter.innerText=target;

                clearInterval(timer);

            }else{

                counter.innerText=current;

            }

        },25);

    });

}

// ============================
// DARK MODE
// ============================

function darkMode(){

    const btn=document.getElementById("themeToggle");

    if(!btn) return;

    if(localStorage.getItem("theme")==="dark"){

        document.body.classList.add("dark");

    }

    btn.onclick=function(){

        document.body.classList.toggle("dark");

        if(document.body.classList.contains("dark")){

            localStorage.setItem("theme","dark");

        }else{

            localStorage.setItem("theme","light");

        }

    }

}

// ============================
// BUTTON EFFECT
// ============================

function smoothButtons(){

    const buttons=document.querySelectorAll(".btn");

    buttons.forEach(btn=>{

        btn.addEventListener("mouseenter",()=>{

            btn.style.transform="translateY(-3px) scale(1.02)";

        });

        btn.addEventListener("mouseleave",()=>{

            btn.style.transform="translateY(0px)";

        });

    });

}

// ============================
// TOOLTIPS
// ============================

function enableTooltips(){

    const tooltipTriggerList=[].slice.call(

        document.querySelectorAll('[data-bs-toggle="tooltip"]')

    );

    tooltipTriggerList.map(function (tooltipTriggerEl) {

        return new bootstrap.Tooltip(tooltipTriggerEl);

    });

}

// ============================
// SUCCESS MESSAGE
// ============================

function showSuccess(message){

    const toast=document.createElement("div");

    toast.className="alert alert-success position-fixed";

    toast.style.right="20px";

    toast.style.bottom="20px";

    toast.style.zIndex="9999";

    toast.innerHTML=message;

    document.body.appendChild(toast);

    setTimeout(()=>{

        toast.remove();

    },2500);

}

document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".btn-danger").forEach(button => {

        button.addEventListener("click", function (e) {

            if (!confirm("Delete this task?")) {

                e.preventDefault();

            }

        });

    });

});