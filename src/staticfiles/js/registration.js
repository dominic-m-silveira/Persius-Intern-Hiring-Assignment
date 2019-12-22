$(function() {
    // We need some mappings for Providers names from AllAuth to the icon class names.
    $('.btn-Google').addClass('btn-google');
    $('.fa-Google').addClass('fa-google');
    $('.btn-GitHub').addClass('btn-github');
    $('.fa-GitHub').addClass('fa-github');
    $('.btn-Bitbucket').addClass('btn-bitbucket');
    $('.fa-Bitbucket').addClass('fa-bitbucket');
    $('.btn-Twitter').addClass('btn-twitter');
    $('.fa-Twitter').addClass('fa-twitter');
console.log('ready');
});

$('#dropdown').hover(function() {
  $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeIn(500);
}, function() {
  $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeOut(500);
});










