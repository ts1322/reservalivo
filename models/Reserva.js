export class Reserva {
constructor({ usuario, livro }) {
this.usuario = usuario;
this.livro = livro;
this.data = new Date().toLocaleDateString();
}
}