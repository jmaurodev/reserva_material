$(document).ready(function(){
  $("#id_identidade_empresta, #id_identidade_retira").on("keypress", function (event){
    if(event.keyCode < 48 || event.keyCode > 57) return false;
  });
  $("#senha_empresta").hide();
  $("#senha_retira").hide();
  $(document).on("keypress", "#id_identidade_empresta", function(){
    $("#senha_empresta").show();
  })
  $(document).on("keypress", "#id_identidade_retira", function(){
    $("#senha_retira").show();
  })
});

$(function(){
  $('#id_filtro_retirou, #id_filtro_emprestou, #id_filtro_material, #id_filtro_numero_serie').keypress(function(event){
    if (event.keyCode == 13){
      $('table tr').not(":first").hide();
      $('input[type=text]').not(this).val('');
      $('table td.col-'+$(this).attr('name')+':contains("'+$(this).val()+'")').parent().fadeIn(3000);
    }
  });
});
