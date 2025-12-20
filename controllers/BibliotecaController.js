import { Usuario } from "../models/Usuario.js";
import { Livro } from "../models/Livro.js";
import { Reserva } from "../models/Reserva.js";


export class BibliotecaController {
constructor(biblioteca, view) {
this.biblioteca = biblioteca;
this.view = view;
}


cadastrarUsuario(dados) {
const usuario = new Usuario(dados);
this.biblioteca.adicionarUsuario(usuario);
this.view.renderUsuarios(this.biblioteca.usuarios);
this.view.renderSelects(this.biblioteca);
}


cadastrarLivro(dados) {
const livro = new Livro(dados);
this.biblioteca.adicionarLivro(livro);
this.view.renderLivros(this.biblioteca.livros);
this.view.renderSelects(this.biblioteca);
}


reservarLivro(indexUsuario, indexLivro) {
const usuario = this.biblioteca.usuarios[indexUsuario];
const livro = this.biblioteca.livros[indexLivro];


if (!livro.disponivel) {
alert("Livro já reservado");
return;
}


const reserva = new Reserva({ usuario, livro });
this.biblioteca.reservarLivro(reserva);


this.view.renderLivros(this.biblioteca.livros);
this.view.renderReservas(this.biblioteca.reservas);
}
}
