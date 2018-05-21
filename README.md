# SisMat
Sistema de controle de material em carga
Utilizado principalmente para material classe VII

# Tarefas imediatas:
Models:
[X] Colocar texto de ajuda nos campos do model
[X] Tornar Pessoa.quartel_atual uma ForeignKey
[X] Setar editable=False para Material.qtd_cautelado e Material.qtd_em_reserva
[X] Remover Material.qtd_siscofis
[X] Ocultar os caracteres dos campos de senha
[ ] Carregar a foto do militar através do DGP
[ ] Inserir CharField com choice status nos materiais: em reserva, cautelado, indisponivel, em manutenção

Views:
[X] Definir base.html
[X] Incluir Navbar
[X] Criar template padrão
[X] Validar campos

Controlers:
[ ] Empréstimo de material, enviando POST para o BD contendo informações e
validando quantitativos e senhas
[ ] Cautelas por pessoa, recebendo pessoa como parâmetro GET
[ ] Destino dos materiais, recebendo material como parâmetro no GET



[ ] Resolver problema da data
[ ] Inserir registro de cautela no banco de dados
