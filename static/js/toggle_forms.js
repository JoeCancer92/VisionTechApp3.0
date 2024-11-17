document.addEventListener("DOMContentLoaded", function () {
    const showLoginButton = document.getElementById('showLoginButton');
    const showRegisterButton = document.getElementById('showRegisterButton');
    const loginFormContainer = document.getElementById('loginFormContainer');
    const registerFormContainer = document.getElementById('registerFormContainer');

    // Mostrar el formulario de inicio de sesión y ocultar el de registro
    showLoginButton.addEventListener('click', function () {
        registerFormContainer.style.display = "none";
        loginFormContainer.style.display = "block";
        loginFormContainer.style.opacity = 0;
        fadeIn(loginFormContainer);
    });

    // Mostrar el formulario de registro y ocultar el de inicio de sesión
    showRegisterButton.addEventListener('click', function () {
        loginFormContainer.style.display = "none";
        registerFormContainer.style.display = "block";
        registerFormContainer.style.opacity = 0;
        fadeIn(registerFormContainer);
    });

    // Función para aplicar el efecto de desvanecimiento
    function fadeIn(element) {
        let opacity = 0;
        element.style.display = "block";
        let interval = setInterval(function () {
            if (opacity < 1) {
                opacity += 0.1;
                element.style.opacity = opacity;
            } else {
                clearInterval(interval);
            }
        }, 50);
    }
});
