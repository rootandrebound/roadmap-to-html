var ALGOLIA_APP_ID = "ER4XGAZU3H";
var ALGOLIA_PUBLIC_KEY = "ad6b289aa74181fef926dc6133bfece7";

function initializeSearch() {
  var searchInput = $('#search-input input[type="text"]');
  var client = algoliasearch(ALGOLIA_APP_ID, ALGOLIA_PUBLIC_KEY);
  var index = client.initIndex('test_ROADMAP');
  searchInput.autocomplete(
    { hint: false },
    [
      {
        source: $.fn.autocomplete.sources.hits(index, { hitsPerPage: 10 }),
        displayKey: 'title',
        templates: {
          suggestion: function(suggestion) {
            var hrefValue = suggestion.path;
            var display = suggestion._highlightResult.title.value;
            var anchorString = '<a href="/roadmap-to-html/' + hrefValue + '">' + display + '</a>';
            return anchorString;
          }
        }
      }
    ]
  );
}


function handleTopPages(topPages){
  var veryTopPages = topPages.slice(1, 6);
  veryTopPages.forEach(function(page){
    $('.popular-pages__list').append(
      '<li class="popular-page"><a href="'+page.url+'">'+page.title+'</a></li>'
    );
  })
}

function pullTopPages(){
  $.getJSON(
    'https://s3.amazonaws.com/rr-roadmap-top-pages-checker/top_pages.json',
    handleTopPages
  );
}

$(function() {
  initializeSearch();
  pullTopPages();

});
