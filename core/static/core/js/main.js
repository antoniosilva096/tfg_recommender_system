document.addEventListener('DOMContentLoaded', () => {
    console.log('Core JavaScript loaded!');


    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    toastElList.forEach(function (toastEl) {
        var toast = new bootstrap.Toast(toastEl);
        toast.show();
    });


    const navLinks = document.querySelectorAll(".navbar-nav .nav-link");
    navLinks.forEach(link => {
        link.addEventListener("click", function () {
            // Remover clase 'active' de todos los enlaces
            navLinks.forEach(link => link.classList.remove("active"));

            // Agregar clase 'active' al enlace actual
            this.classList.add("active");

            // Guardar en sessionStorage el enlace seleccionado
            sessionStorage.setItem("activeLink", this.href);
        });
       
    const activeLinkHref = sessionStorage.getItem("activeLink");
    if (activeLinkHref) {
        const activeLink = [...navLinks].find(link => link.href === activeLinkHref);
        if (activeLink) {
            activeLink.classList.add("active");
        }
    }
    });
  

});


// static/js/loader.js
window.addEventListener("pageshow", function(event) {
    const loader = document.getElementById("loader");
    if (event.persisted) {
        // Si la página fue cargada desde el caché, ocultamos el loader
        if (loader) {
            loader.classList.remove("d-flex"); 
            loader.style.display = "none";
            document.body.style.overflowY = ''; 
        }
    } else {
        
        if (loader) {
            loader.classList.remove("d-flex");
            loader.style.display = "none";
            document.body.style.overflowY = ''; 
        }
    }
});

window.addEventListener("beforeunload", function() {
    const loader = document.getElementById("loader");
    if (loader) {
        loader.classList.add("d-flex"); 
        loader.style.display = "flex";
        document.body.style.overflowY = 'hidden'; 
    }
});


document.addEventListener("DOMContentLoaded", function() {
    const loginCard = document.getElementById("login-card");
    const alertDanger = document.querySelector(".alert-danger");

    if (alertDanger) {
        loginCard.classList.add("shake");
        loginCard.addEventListener("animationend", () => {
            loginCard.classList.remove("shake");
        });
    }
});

