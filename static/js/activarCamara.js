// Archivo: activarCamara.js

document.addEventListener('DOMContentLoaded', function () {
    // Configuración para activar/desactivar la cámara en el formulario de registro
    const activarCamaraRegisterButton = document.getElementById('activarCamaraRegisterButton');
    const videoRegister = document.getElementById('videoRegister');
    let registerStream = null;

    activarCamaraRegisterButton.addEventListener('click', () => {
        if (registerStream) {
            // Desactivar la cámara
            registerStream.getTracks().forEach(track => track.stop());
            videoRegister.srcObject = null;
            videoRegister.style.display = 'none';
            activarCamaraRegisterButton.textContent = 'Activar Cámara';
            registerStream = null;
        } else {
            // Activar la cámara
            navigator.mediaDevices.getUserMedia({ video: true })
                .then((stream) => {
                    registerStream = stream;
                    videoRegister.srcObject = stream;
                    videoRegister.style.display = 'block'; // Mostrar el video después de activar la cámara
                    activarCamaraRegisterButton.textContent = 'Desactivar Cámara';
                })
                .catch((err) => {
                    console.error("Error al acceder a la cámara para registro:", err);
                    alert("Error al acceder a la cámara. Por favor, verifica tu configuración.");
                });
        }
    });

    // Configuración para activar/desactivar la cámara en el formulario de inicio de sesión
    const activarCamaraLoginButton = document.getElementById('activarCamaraLoginButton');
    const videoLogin = document.getElementById('videoLogin');
    let loginStream = null;

    activarCamaraLoginButton.addEventListener('click', () => {
        if (loginStream) {
            // Desactivar la cámara
            loginStream.getTracks().forEach(track => track.stop());
            videoLogin.srcObject = null;
            videoLogin.style.display = 'none';
            activarCamaraLoginButton.textContent = 'Activar Cámara';
            loginStream = null;
        } else {
            // Activar la cámara
            navigator.mediaDevices.getUserMedia({ video: true })
                .then((stream) => {
                    loginStream = stream;
                    videoLogin.srcObject = stream;
                    videoLogin.style.display = 'block'; // Mostrar el video después de activar la cámara
                    activarCamaraLoginButton.textContent = 'Desactivar Cámara';
                })
                .catch((err) => {
                    console.error("Error al acceder a la cámara para inicio de sesión:", err);
                    alert("Error al acceder a la cámara. Por favor, verifica tu configuración.");
                });
        }
    });

    // Configuración para capturar la imagen antes de iniciar sesión
    const loginButton = document.getElementById('loginButton');
    const canvasLogin = document.getElementById('canvasLogin');
    const imagenLoginInput = document.getElementById('imagenLogin');

    loginButton.addEventListener('click', () => {
        if (!loginStream) {
            alert("Por favor, activa la cámara para poder iniciar sesión.");
            return;
        }

        const usuario = document.getElementById('usuario').value;
        const contrasena = document.getElementById('contrasenaLogin').value;

        if (usuario === "" || contrasena === "") {
            alert("Por favor, completa todos los campos requeridos.");
            return;
        }

        // Mostrar spinner de carga en el botón
        loginButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Iniciando...';

        const context = canvasLogin.getContext("2d");
        canvasLogin.width = videoLogin.videoWidth;
        canvasLogin.height = videoLogin.videoHeight;
        context.drawImage(videoLogin, 0, 0, canvasLogin.width, canvasLogin.height);

        const dataUrl = canvasLogin.toDataURL("image/jpeg");
        imagenLoginInput.value = dataUrl;

        // Enviar el formulario de inicio de sesión
        document.getElementById("loginForm").submit();
    });

    // Configuración para capturar la imagen antes de registrar usuario
    const registerButton = document.getElementById('registerButton');
    const canvasRegister = document.getElementById('canvasRegister');
    const imagenRegisterInput = document.getElementById('imagenRegister');

    registerButton.addEventListener('click', () => {
        if (!registerStream) {
            alert("Por favor, activa la cámara para poder registrarte.");
            return;
        }

        const nombre = document.getElementById("nombre").value;
        const apellido = document.getElementById("apellido").value;

        if (nombre === "" || apellido === "") {
            alert("Por favor, completa todos los campos requeridos.");
            return;
        }

        // Mostrar spinner de carga en el botón
        registerButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Registrando...';

        const context = canvasRegister.getContext("2d");
        canvasRegister.width = videoRegister.videoWidth;
        canvasRegister.height = videoRegister.videoHeight;
        context.drawImage(videoRegister, 0, 0, canvasRegister.width, canvasRegister.height);

        const dataUrl = canvasRegister.toDataURL("image/jpeg");
        imagenRegisterInput.value = dataUrl;

        // Enviar el formulario de registro
        document.getElementById("registerForm").submit();
    });
});
