export class Biblioteca {
constructor() {
this.usuarios = [];
this.livros = [];
this.reservas = [];
}


adicionarUsuario(usuario) {
this.usuarios.push(usuario);
}


adicionarLivro(livro) {
this.livros.push(livro);
}


reservarLivro(reserva) {
reserva.livro.disponivel = false;
this.reservas.push(reserva);
}
}