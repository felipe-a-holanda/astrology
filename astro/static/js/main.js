
Number.prototype.mod = function(n) {
    return ((this%n)+n)%n;
}





function saveChart(){
    var date = $('#datepicker').data().date;
    var time = $('#timepicker').data().date;
    var location = $('#locationpicker').val();
    var name = $('#namepicker').val();
    msg = "Name: "+name+"\n" +"Date: "+date+'\n'+"Time: "+time+'\n'+"Location: "+location;


    data = {
        'name': name,
        'date': date,
        'time': time,
        'location': location,
    }

    $.ajax({
        type: "POST",
        url: url_save_chart(),
        data: data,
        });

}

function updateTime(){
    date = $('#datepicker').data('DateTimePicker').date();
    time = $('#timepicker').data('DateTimePicker').date();
    city = $('#location-input').val();

    if (date){date = date.format('DD-MM-YYYY');}
    else{date = "";}

    if (time){time = time.format('HH:mm');}
    else{time = "";}
    datetime = date+"_"+time;

    move_svg(date, time, city);
    //$('div#chart').load('/horoscope/chart/?&date='+date+'&time='+time+'');

}

function loadInitial(){
    updateTime();

}

function load_chart(){
    var s = Snap("#svgout");
    var g = s.group();
    var chart = Snap.load("static/img/chart.svg", function ( loadedFragment ) {
                                                    g.append( loadedFragment );
                                                    loadInitial();
                                            } );
}


$(document).ready(function() {
    load_chart();
});


function polar2rect(x0, y0, radius, angle_deg){
    var angle_rad = Math.PI - angle_deg*Math.PI/180.0;
    var x = x0 + radius*Math.cos(angle_rad);
    var y = y0 + radius*Math.sin(angle_rad);
    return {x:x, y:y};
}



function aspect_type(a1, a2){
    diff = Math.min(360-Math.abs(a1-a2), Math.abs(a1-a2));
    var t1 = ((diff / 30) >> 0)*30;
    var d1 = diff.mod(30);

    var t2 = Math.abs(Math.floor(diff / -30)) * 30;
    var d2 = Math.abs(diff.mod(-30));

    if (d1<d2){
        var t = t1;
        var d = d1;
    }else{
        var t = t2;
        var d = d2;
    }

    return {type:t, orb:d};
}


function aspect_force(a1, a2){
    var t = aspect_type(a1, a2);
    var type = t.type;
    var orb = t.orb;
    var max_orb = 10;


    var stroke = 'none';
    var stroke_width = 1;
    var stroke_opacity = 1;

    if (type==0 || type==60 || type==120){stroke='blue';}
    if (type==90 || type==180){stroke='red';}

    stroke_opacity = max_orb - orb;
    if (stroke_opacity<0){
        stroke_opacity = 0;
        stroke='none';
    }
    if (orb<5){
        stroke_width = Math.floor(5 - orb)
        if (stroke_width<=0){
            stroke_width = 0;
            stroke='none';

        }
    }

    if (orb>max_orb){stroke='none';}


    return {'stroke':stroke, 'stroke_opacity':stroke_opacity, 'stroke_width':stroke_width};
}


function move_svg(date, time, city){
    var s = Snap("#svgout");

    $.get( "/horoscope/eph/?date="+date+"&time="+time+'&city='+city, function(data) {
        move_planets(s, data);
        move_aspects(s, data);
        if (data.houses) move_houses(s, data.houses);

       }, 'json')
}



function move_aspects(s, data){
    asc = 0;
    if (data.houses) asc = data.houses[0];

    planets = data.planets;
    for(i=0;i<planets.length;i++){
       for(j=0;j<planets.length;j++){
            if(j>i){
                var a1 = planets[i].angle - asc;
                var a2 = planets[j].angle - asc;
                var p1 = polar2rect(300, 300, 200, a1);
                var p2 = polar2rect(300, 300, 200, a2);
                var aspect_name = planets[i].name + '_' + planets[j].name + '_aspect';
                var line = s.select('#'+aspect_name);

                aspect = aspect_force(a1,a2);
                if(line){
                    line.attr({x1:p1.x, y1:p1.y, x2:p2.x, y2:p2.y, stroke: aspect.stroke, 'stroke-opacity':aspect.stroke_opacity, 'stroke-width':aspect.stroke_width});

                }else{
                    s.line(p1.x,p1.y,p2.x,p2.y).attr({id:aspect_name, stroke: aspect.stroke, 'stroke-opacity':aspect.stroke_opacity, 'stroke-width':aspect.stroke_width});

                }

            }
        }
    }
}

function move_planets(s, data){
    asc = 0;
    planets = data.planets;
    if (data.houses) asc = data.houses[0]
    $.each(planets, function(index, planet_data){
        planet_name = planet_data.name;
        planet_angle = planet_data.angle - asc;

        var planet_id = "#"+planet_name;

        var planet = s.select(planet_id);
        if (planet){
            point = polar2rect(0, 0, 220, planet_angle);
            planet.attr({'x':point.x, 'y':point.y, 'visibility':'visible'});
        }
    })
}

function move_houses(s, houses){
    asc = houses[0];
    s.select('#zodiac').transform('r'+asc+',300,300');
    for(i=0; i<12; i++){
        var line = s.select('#house_'+(i+1));
        var angle = houses[i] - asc;
        var p1 = polar2rect(300, 300, 200, angle);
        var p2 = polar2rect(300, 300, 240, angle);

        if (i%4==0) line.attr({'stroke-width':2});
        if (i==0) {
            p1 = polar2rect(300, 300, 200, angle);
            p2 = polar2rect(300, 300, 250, angle);
            line.attr({'stroke-width':3});
        }
        line.attr({x1:p1.x, y1:p1.y, x2:p2.x, y2:p2.y});

    }
}






// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});