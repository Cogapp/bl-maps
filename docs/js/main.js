
    // convenience functions
    $.urlParam = function(name){
        var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
        if (results==null){
            return null;
        }
        else{
            return results[1] || 0;
        }
    }

    $.getCoords = function(name) {
        $.each(window.ocr.responses[0].textAnnotations, function(i, v) {
            if (v.description == name) {
                console.log(v.boundingPoly);
                return;
            }
        });

    }

    $.createSidePanel = function(index) {
        var data = window.ocr[index];
        var desc = '<h2>' + data.name + '</h2> \
                    <ul>';

        if (data.name != data.toponymName) {
            desc += '<li>Alternate name: ' + data.toponymName + '</li>';
        }

        desc +=    '<li>Population: ' + data.population + '</li> \
                    <li>Country: ' + data.countryName + '</li> \
                    <li>(From OCR: ' + data.description + ')</li> \
                    </ul>';

        $('.info-panel').html(desc)
    }

    $.destroySidePanel = function() {
        $('.info-panel').html('');
    }

        // error trap
    if (!$.urlParam('id')) {
        alert ('you must specify a map ID in the query string. E.g. ?id=IOR_L_PS_10_595_0243')
    }
    var mapID = $.urlParam('id')
    console.log($.urlParam('id'));

    // load viewer
    var viewer = OpenSeadragon({
        id: "openseadragon1",
        prefixUrl: "/openseadragon-bin-2.4.0/images/",
        tileSources: "http://hsimages.cogapp.com:8182/iiif/2/cogapp_hackday%2FWar_Office_Maps%2F" + $.urlParam('id') + ".ptif/info.json"
    }).addHandler('open', function(e){
        var viewer = e.eventSource

        // load data from file
        $.getJSON('data/places_json/' + mapID + '.ptif.json', function(json) {
            console.log(json);
            window.ocr = json;

            // create overlays
            $.each(window.ocr, function(i, v) {
                var o = v
                if (o && 'xywh' in o) {
                    console.log('Location: ' + o['toponymName'] + ', ' + o['name'] + '. Population: ' + o['population']);
                    var elt = document.createElement("div");
                    elt.id = "runtime-overlay";
                    elt.className = "highlight";
                    elt.setAttribute('data-idx', i);
                    viewer.addOverlay({
                        element: elt,
                        location: viewer.viewport.imageToViewportRectangle(new OpenSeadragon.Rect(o['xywh']['x'], o['xywh']['y'], o['xywh']['w'], o['xywh']['h']))
                    });
                    new OpenSeadragon.MouseTracker({
                        element: elt,
                        enterHandler: function(e) {
                            $.createSidePanel(elt.getAttribute('data-idx'))
                        },
                        exitHandler: function(e) {
                            $.destroySidePanel();
                        },
                    });

                }
            });


        });




    });
