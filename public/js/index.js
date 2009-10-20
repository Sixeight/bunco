Hatena.Star.Token = 'dfe73460b07ea3bf681104e615d5ecd85df02e2e';
Hatena.Star.SiteConfig = {
    entryNodes: {
        'tr.book': {
            uri: 'span.title a',
            title: 'span.title a',
            container: 'span.title'
        }
    }
};


$(function() {
      $("#index .newbook .trigger").click(function() {
          $(this).remove();
          $(".form", $(this).parent().get(0)).show();
      });
});