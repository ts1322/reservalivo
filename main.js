import { Biblioteca } from "./models/Biblioteca.js";
import { BibliotecaController } from "./controllers/BibliotecaController.js";
import { BibliotecaView } from "./views/BibliotecaView.js";


const biblioteca = new Biblioteca();
const view = new BibliotecaView();
const controller = new BibliotecaController(biblioteca, view);


// USUÁRIO
const formUsuario = document.getElementById("form-usuario");
formUsuario.addEventListener("submit", e => {
e.preventDefault();
controller.cadastrarUsuario({
nome: formUsuario.nome.value,
email: formUsuario.email.value
});
formUsuario.reset();
});


// LIVRO
const formLivro = document.getElementById("form-livro");
formLivro.addEventListener("submit", e => {
e.preventDefault();
controller.cadastrarLivro({
titulo: formLivro.titulo.value,
autor: formLivro.autor.value
});
formLivro.reset();
});


// RESERVA
const formReserva = document.getElementById("form-reserva");
formReserva.addEventListener("submit", e => {
e.preventDefault();
controller.reservarLivro(
formReserva.usuario.value,
formReserva.livro.value
);
});