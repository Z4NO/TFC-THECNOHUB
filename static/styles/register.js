document.addEventListener('DOMContentLoaded', function () {

  const registerContainer = document.getElementById('register-container');
  const loginContainer = document.getElementById('login-container');
  const finalContainer = document.getElementById('final-container');
  const nextToLogin = document.getElementById('next-to-login');
  const prevToRegister = document.getElementById('prev-to-register');
  const nextToFinal = document.getElementById('next-to-final');
  const prevToLoginFinal = document.getElementById('prev-to-login-final');

  

  nextToLogin.addEventListener('click', function () {
    // Tenemos que validar que ha relleneado el formulario de registro de email y contraseña , además de que los campos de contraseña y confirmar contraseña son iguales
    if( !document.getElementById('email').value.trim() || !document.getElementById('contrasena').value.trim()  || !document.getElementById('confirm').value.trim() ) {
      alert('Por favor, rellena todos los campos');
      return;
    }else{
      var strongRegex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\\$%\^&\*])(?=.{8,})");
      
      const password = document.getElementById('contrasena').value.trim();
      const confirmPassword = document.getElementById('confirm').value.trim();
      if(!strongRegex.test(password)) {
        alert("La contraseña no sigue el patron establecido")
        return;
      }
      if (password !== confirmPassword) {
        alert('Las contraseñas no coinciden');
        return;
      }
      registerContainer.style.display = 'none';
      loginContainer.style.display = 'block';
    }
  });

  prevToRegister.addEventListener('click', function () {
    if(!document.getElementById('nombre').value.trim()){
      alert('Por favor, rellena el campo de nombre');
      return;
    }else{
      if(document.getElementById('nombre').value.trim().length < 3){
        alert('El nombre debe tener al menos 3 caracteres');
        return;
      }
      loginContainer.style.display = 'none';
      registerContainer.style.display = 'block';
    }
  });

  nextToFinal.addEventListener('click', function () {
    loginContainer.style.display = 'none';
    finalContainer.style.display = 'block';
  });

  prevToLoginFinal.addEventListener('click', function () {
    finalContainer.style.display = 'none';
    loginContainer.style.display = 'block';
  });

});