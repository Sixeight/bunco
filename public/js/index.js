Hatena.Star.Token = 'dfe73460b07ea3bf681104e615d5ecd85df02e2e';
Hatena.Star.SiteConfig = {
    entryNodes: {
        '.book': {
            uri: '.label a',
            title: '.about .title',
            container: '.about .title'
        },
        '.activity': {
            uri: '.hidden-key',
            title: '.title',
            container: '.title'
        }
    }
};

$(function() {
      $("#index .newbook .trigger").click(function() {
          $(this).remove();
          $(".form", $(this).parent().get(0)).show();
      });
});