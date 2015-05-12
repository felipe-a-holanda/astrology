$(function(){
    var locationPicker = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    //prefetch: '/data/prefetch/',
    remote: '/geocode/?query=%QUERY'
    });

    locationPicker.initialize();

    $('#location').typeahead(null, {
      name: 'best-pictures',
      displayKey: 'value',
      hint: true,
      highlight: true,
      minLength: 2,
      source: locationPicker.ttAdapter()
    });


});
