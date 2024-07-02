$(document).ready(function () {
    $("#klasifikasi_perkara").prop("disabled", true);

    $('#jenis_perkara').change(function () {

        $("#klasifikasi_perkara").prop("disabled", true);

        var jenis_perkara_id = $('#jenis_perkara').val();

        // Make Ajax Request and expect JSON-encoded data
        $.getJSON('/ref/klasifikasi-perkara/get/'+ jenis_perkara_id, function (data) {

            // Remove old options
            $('#klasifikasi_perkara').find('option').remove();

            // Add new items
            $.each(data, function (key, val) {
                var option_item = '<option value="' + val.id + '">' + val.name + '</option>'
                $('#klasifikasi_perkara').append(option_item);
                $("#klasifikasi_perkara").prop("disabled", false);
            });
        });
    });

});
//     $("#city").prop("disabled", true);
//     $("#district").prop("disabled", true);
//     $("#village").prop("disabled", true);
//     $("#address").prop("disabled", true);

//     $('#province').change(function () {

//         $("#city").prop("disabled", true);
//         $("#district").prop("disabled", true);
//         $("#village").prop("disabled", true);
//         $("#address").prop("disabled", true);

//         var prov_id = $('#province').val();
//         console.log(prov_id);

//         // Make Ajax Request and expect JSON-encoded data
//         $.getJSON(
//             '/get_city' + '/' + prov_id,
//             function (data) {

//                 // Remove old options
//                 $('#city').find('option').remove();

//                 // Add new items
//                 $.each(data, function (key, val) {
//                   var option_item = '<option value="' + val.city_id + '">' + val.city_name + '</option>'
//                   $('#city').append(option_item);
//                   $("#city").prop("disabled", false);
//                 });
//             }
//         );
//     });
//     $('#city').change(function () {

//         $("#district").prop("disabled", true);
//         $("#village").prop("disabled", true);
//         $("#address").prop("disabled", true);

//         var city_id = $('#city').val();
//         console.log(city_id);

//         // Make Ajax Request and expect JSON-encoded data
//         $.getJSON(
//             '/get_dis' + '/' + city_id,
//             function (data) {

//                 // Remove old options
//                 $('#district').find('option').remove();

//                 // Add new items
//                 $.each(data, function (key, val) {
//                   var option_item = '<option value="' + val.dis_id + '">' + val.dis_name + '</option>'
//                   $('#district').append(option_item);
//                   $("#district").prop("disabled", false);
//                 });
//             }
//         );
//     });
//     $('#district').change(function () {

//         $("#village").prop("disabled", true);
//         $("#address").prop("disabled", true);

//         var dis_id = $('#district').val();
//         console.log(dis_id);

//         // Make Ajax Request and expect JSON-encoded data
//         $.getJSON(
//             '/get_subdis' + '/' + dis_id,
//             function (data) {

//                 // Remove old options
//                 $('#village').find('option').remove();

//                 // Add new items
//                 $.each(data, function (val) {
//                   var option_item = '<option value="' + val.subdis_id + '">' + val.subdis_name + '</option>'
//                   $('#village').append(option_item);
//                   $("#village").prop("disabled", false);
//                   $("#address").prop("disabled", false);
//                 });
//             }
//         );
//     });
//     // $('#defaultModal').on('hidden.bs.modal', function () {
//     //     location.reload(true);
//     // })
