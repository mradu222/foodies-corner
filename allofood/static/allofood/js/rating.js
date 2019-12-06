$(document).ready(function () {

    var srcIn = 'fa fa-star star'; //image au survol
    var srcOut = 'fa fa-star-o star'; // image non survolÃ©e
    var note = 0;

    // Obtenir id numÃ©rique des Ã©toiles au format star_numero
    function idNum(id) {
        var id = id.split('_');
        var id = id[1];
        return id;
    }

    //  Survol des Ã©toiles
    $('.star').click(function () {
        if (note == 0) {
            note = idNum($(this).attr('id'));
            $("#stars").attr("value", note);
//		alert($("#stars").val());
        } else {
            note = 0;
        }
    });

    $('.star').hover(function () {
        if (note == 0) {

            var id = idNum($(this).attr('id')); // id numÃ©rique de l'Ã©toile survolÃ©e
            var i; // Variable d'incrÃ©mentation

            for (i = 1; i <= 5; i++) {
                if (i <= id) {
                    $('#star_' + i).attr({class: srcIn});
                } else if (i > id) $('#star_' + i).attr({class: srcOut});
            }
        }
    }, function () {
    });

    $('.giving').click(function (e) {
        if ($(".ecrire-avis").val().length < 4) {
            e.preventDefault();
        }
    });

});


$(document).ready(function () {
    var $myForm = $('#comment_form')
    $myForm.submit(function (event) {
        event.preventDefault()
        var $formData = $(this).serialize()
        var $thisURL = $myForm.attr('data-url')
        $.ajax({
            method: "POST",
            url: $thisURL,
            data: $formData,
            success: handleFormSuccess,
            error: handleFormError,
        })
    })

    function handleFormSuccess(data, textStatus, jqXHR) {

        $myForm[0].reset(); // reset form data

        var rating = '';
        for (var i = 0; i < data.stars; i++) {
            rating += '<span class="fa fa-star " id="star_1_1" style="color:tomato;"></span>'
        }
        for (var i = data.stars; i < 5; i++) {
            rating += '<span class="fa fa-star-o star" id="star_5_1" style="color:tomato;"></span>'
        }

        var newComment = '<div class="">' +
            '                        <div class="col-md-12 row">' +
            '                            <div class="col-md-1" style="width:100%;"><img' +
            '                                    style="width:100%;margin-top:25px;border-radius:50%;"' +
            '                                    src="/static/allofood/images/avatar.png">' +
            '                            </div>' +
            '                            <div class="col-md-11">' +
            '                                <div class="col-md-12 titre-avis">' +
            '                                    <p class="" name="username" style="">' + data.username + '</p>' +
            '                                    <div class="rating" style="margin-top:-18px;">' + rating +
            '                                    </div>' +
            '                                </div>' +
            '                                <div class="col-md-12" style="background-color:beige;">' +
            '                                    <p style="height:10%;width:100%;margin-top:15px;"' +
            '                                       name="comment">' + data.text + '</p>' +
            '                                </div>' +
            '                            </div>' +
            '                        </div>' +
            '                    </div>';
        $(".avis").append(newComment)
    }

    function handleFormError(jqXHR, textStatus, errorThrown) {
    }
})

