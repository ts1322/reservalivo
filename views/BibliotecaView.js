export class BibliotecaView {
constructor() {
this.listaUsuarios = document.getElementById("lista-usuarios");
this.listaLivros = document.getElementById("lista-livros");
this.listaReservas = document.getElementById("lista-reservas");


this.selectUsuario = document.getElementById("select-usuario");
this.selectLivro = document.getElementById("select-livro");
}


renderUsuarios(usuarios) {
this.listaUsuarios.innerHTML = "";
usuarios.forEach(u => {
const li = document.createElement("li");
li.textContent = `${u.nome} - ${u.email}`;
this.listaUsuarios.appendChild(li);
});
}


renderLivros(livros) {
this.listaLivros.innerHTML = "";
livros.forEach(l => {
const li = document.createElement("li");
li.textContent = `${l.titulo} - ${l.autor} | ${l.disponivel ? "Disponível" : "Reservado"}`;
this.listaLivros.appendChild(li);
});
}


renderReservas(reservas) {
this.listaReservas.innerHTML = "";
reservas.forEach(r => {
const li = document.createElement("li");
li.textContent = `${r.usuario.nome} reservou '${r.livro.titulo}' em ${r.data}`;
this.listaReservas.appendChild(li);
});
}


renderSelects(biblioteca) {
this.selectUsuario.innerHTML = "";
this.selectLivro.innerHTML = "";


biblioteca.usuarios.forEach((u, i) => {
const opt = document.createElement("option");
opt.value = i;
opt.textContent = u.nome;
this.selectUsuario.appendChild(opt);
});


biblioteca.livros.forEach((l, i) => {
const opt = document.createElement("option");
opt.value = i;
opt.textContent = l.titulo;
this.selectLivro.appendChild(opt);
});
}
}
