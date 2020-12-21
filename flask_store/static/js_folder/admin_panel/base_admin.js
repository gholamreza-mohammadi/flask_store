$(function () {
    function data_div_cleaner() {
        if ($("div#table_div").children().length) {
            $("div#header_div").empty();
            $("div#table_div").empty();
        }
    }

    $("a#product").click(function (event) {
        event.preventDefault();
        $.post("product-api", function (response, status) {
            data_div_cleaner();
            if (status == "success") {
                var header = "<h2>مدیریت کالاها</h2>";
                header += "<div>";
                header += '<a href="" class="btn_a" id="add_products_btn">import</a> ';
                header += '<a href="" class="btn_a" id="add_product_btn">افزودن کالا</a>';
                header += "</div>";

                var column_names = response.column_names;
                var table = "<table>";
                table += "<tr>";
                table += "<th>" + "تصویر" + "</th>";
                table += "<th>" + "نام کالا" + "</th>";
                table += "<th>" + "دسته بندی" + "</th>";
                table += "<th>" + " " + "</th>";
                table += "</tr>";

                var counter = 0;
                response.data.forEach(function (element) {
                    table += "<tr>";
                    table += "<td><a href=" + element[column_names[0]] + " target='_blank'>link</a></td>";
                    table += "<td>" + element[column_names[1]] + "</td>";
                    table += "<td>" + element[column_names[2]] + "</td>";
                    table += '<td><a href="#" id="product_edit_' + counter + '">ویرایش</a> ';
                    table += '<a href="#" id="product_delete_' + counter + '">حذف</a></td>';
                    table += "</tr>";
                    counter++;
                });
                table += "</table>";

                $("div#header_div").append(header);
                $("div#table_div").append(table);

                $("a#add_product_btn").click(function (event) {
                    event.preventDefault();
                    $.post("category-api", function (response, status) {
                        if (status == "success") {
                            if ($("div#popup_div").children().length) {
                                // for closing
                                $("div#popup_div").empty();
                            }

                            var popup = '<div class="popup">';
                            popup += "<h2>افزودن / ویرایش کالا</h2>";
                            popup += "<h4>نام کالا:</h4>";
                            popup += '<input type="text" id="product_name" name="product_name"><br>';
                            popup += "<h4>دسته بندی:</h4>";
                            popup += '<select name="product_category" id="product_category">';
                            response.data.forEach(function (element) {
                                popup += "<option value=" + element + ">" + element + "</option>";
                            });
                            popup += "</select><br>";
                            popup += '<div class="container"><a href="#" class="btn_a" id="add_products_btn">ذخیره</a></div>';
                            popup += "</div>";

                            $("div#popup_div").append(popup);
                            $("div.popup").lightbox_me();
                        } else {
                            alert("Error in received data.");
                        }
                    });
                });

                $("a#add_products_btn").click(function (event) {
                    event.preventDefault();
                    var popup = '<div class="popup">';
                    popup += "<h2>آپلود فایل جدول کالا</h2>";
                    popup += "<h4>انتخاب فایل:</h4>";
                    popup += '<input id="products_file" name="products_file" type="file">';
                    popup += '<div class="container"><a href="#" class="btn_a" id="add_products_btn">آپلود و ذخیره‌سازی جدول</a></div>';
                    popup += "</div>";

                    $("div#popup_div").append(popup);
                    $("div.popup").lightbox_me();
                });
            } else {
                $("div#table_div").append("Error in page loading.");
            }
        });
    });
});
