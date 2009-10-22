Hatena.Star.Token = 'dfe73460b07ea3bf681104e615d5ecd85df02e2e';
Hatena.Star.SiteConfig = {
    entryNodes: {
        '.book': {
            uri: '.label a',
            title: '.about .title',
            container: '.about .title'
        }
    }
};

Hatena.Star.EntryLoader.loadEntries = function(node) {
    var c = Hatena.Star.EntryLoader;
    var entries = c.loadEntriesByConfig(node);
    
    $(".activity", node).each(function() {
        var e = {entryNode: this};
        e.title = $(".title", this).text();
        e.uri = "http://hacobunko.appspot.com/activity/" + $(".key", this).text();
        e.comment_container = c.createCommentContainer();
        $(".title", this).append(e.comment_container);
        e.star_container = c.createStarContainer();
        $(".title", this).append(e.star_container);
        entries.push(e);
    });
    return entries;
};


$(function() {
      $("#index .newbook .trigger").click(function() {
          $(this).remove();
          $(".form", $(this).parent().get(0)).show();
      });
});