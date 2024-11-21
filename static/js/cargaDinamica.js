$(document).ready(function () {
    $('#gestionarUsuariosButton').on('click', function (event) {
        event.preventDefault();
        console.log("Clic en el botón 'Gestión de Usuarios' detectado.");

        // Hacer la solicitud para cargar gestionar usuarios
        $.get('/gestionar_usuarios', function (data) {
            $('#main-content').html(data);
            console.log("Contenido de gestión de usuarios cargado.");

            // Después de cargar la página, ejecutar todos los scripts que contiene.
            $('#main-content').find('script').each(function () {
                $.globalEval(this.text || this.textContent || this.innerHTML || '');
            });
        }).fail(function () {
            console.error('Error al cargar la página de gestionar usuarios.');
        });
    });
});
