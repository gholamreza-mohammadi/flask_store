$(function () {
    function data_div_cleaner() {
        if ($("div#table_div").children().length) {
            $("div#header_div").empty();
            $("div#table_div").empty();
        }
    }

    $("a#product").click(function (event) {
        event.preventDefault();
        $.post("get-products", function (response, status) {
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

                var products_obj = {};
                response.data.forEach(function (element) {
                    table += "<tr>";
                    table += "<td><a href=" + element[column_names[1]] + " target='_blank'>link</a></td>";
                    table += "<td>" + element[column_names[2]] + "</td>";
                    table += "<td>" + element[column_names[3]] + "</td>";
                    table += '<td><a href="" class="edit_product" id="edit_product_' + element[column_names[0]] + '">ویرایش</a> ';
                    products_obj['edit_product_' + element[column_names[0]]] = element[column_names[0]];
                    table += '<a href="" class="delete_product" id="delete_product_' + element[column_names[0]] + '">حذف</a></td>';
                    products_obj['delete_product_' + element[column_names[0]]] = element[column_names[0]];
                    table += "</tr>";
                });
                table += "</table>";

                $("div#header_div").append(header);
                $("div#table_div").append(table);

                $("a#add_product_btn").click(function (event) {
                    event.preventDefault();
                    $.post("category-api", function (response, status) {
                        if (status == "success") {
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
                            popup += '<div class="container"><a href="" class="btn_a" id="save_product_btn">ذخیره</a></div>';
                            popup += "</div>";

                            $("div#popup_div").append(popup);
                            $("div.popup").lightbox_me();

                            $("a#save_product_btn").click(function (event) {
                                event.preventDefault();
                                if ($('input#product_name').val().length) {
                                    $.ajax({
                                        type: 'POST',
                                        contentType: 'application/json',
                                        url: 'set-product',
                                        dataType : 'json',
                                        data : JSON.stringify({"add_product": true,
                                                               "product_name": $('input#product_name').val(),
                                                               "product_category": $('select#product_category').find(":selected").text()}),
                                        success : function (result) {
                                            console.log(result);
                                        }, error : function (result) {
                                            console.log(result);
                                        }   
                                    });
                                    $("div.popup").trigger('close');
                                } else {
                                    console.log('error'); // input name red color
                                }
                            });

                        } else {
                            alert("Error in received data.");
                        }
                    });
                });

                $("a#add_products_btn").click(function (event) {
                    event.preventDefault();
                    var popup = '<div class="popup">';
                    popup += "<h2>آپلود فایل جدول کالا</h2>";
                    popup += "<h4>انتخاب فایل.......:</h4>";
                    // popup += '<div dir="ltr"><input dir="ltr" id="products_file" name="products_file" type="file"></div>';
                    // popup += '<div class="container"><a href="" class="btn_a" id="save_products_btn">آپلود و ذخیره‌سازی جدول</a></div>';
                    popup += '<form method="POST" enctype="multipart/form-data" id="fileUploadForm">';
                    popup += '<div dir="ltr"><input dir="ltr" id="products_file" name="products_file" type="file"></div>';
                    popup += '<div class="container"><button type="submit">آپلود و ذخیره‌سازی جدول</button></div></form>';
                    popup += "</div>";

                    $("div#popup_div").append(popup);
                    $("div.popup").lightbox_me();

                    $('button[type=submit]').click(function (event) {
                        event.preventDefault();
                        if ($('input#products_file').val().length) {
                            $.ajax({
                                type: 'POST',
                                enctype: 'multipart/form-data',
                                url: 'set-product',
                                data: new FormData($('#fileUploadForm')[0]),
                                processData: false,
                                contentType: false,
                                cache: false
                            });
                            $("div.popup").trigger('close');
                        }
                    });
                });

                $("a.edit_product").click(function (event) {
                    event.preventDefault();
                    var p_id = products_obj[$(this).attr("id")];
                    $.post("category-api", function (response, status) {
                        if (status == "success") {
                            var popup = '<div class="popup">';
                            popup += "<h2>افزودن / ویرایش کالا</h2>";
                            popup += "<h4>نام کالا:</h4>";
                            popup += '<input type="text" id="edit_product_name" name="product_name"><br>';
                            popup += "<h4>دسته بندی:</h4>";
                            popup += '<select name="product_category" id="edit_product_category">';
                            response.data.forEach(function (element) {
                                popup += "<option value=" + element + ">" + element + "</option>";
                            });
                            popup += "</select><br>";
                            popup += '<div class="container"><a href="" class="btn_a" id="save_edited_product_btn">ذخیره</a></div>';
                            popup += "</div>";

                            $("div#popup_div").append(popup);
                            $("div.popup").lightbox_me();

                            $("a#save_edited_product_btn").click(function (event) {
                                event.preventDefault();
                                if ($('input#edit_product_name').val().length) {
                                    $.ajax({
                                        type: 'POST',
                                        contentType: 'application/json',
                                        url: 'set-product',
                                        dataType : 'json',
                                        data : JSON.stringify({"edit_product": true,
                                                               "product_id": p_id,
                                                               "product_name": $('input#edit_product_name').val(),
                                                               "product_category": $('select#edit_product_category').find(":selected").text()}),
                                        success : function (result) {
                                            console.log(result);
                                        }, error : function (result) {
                                            console.log(result);
                                        }   
                                    });
                                    $("div.popup").trigger('close');
                                } else {
                                    console.log('error'); // input name red color
                                }
                            });

                        } else {
                            alert("Error in received data.");
                        }
                    });
                });

                $("a.delete_product").click(function (event) {
                    event.preventDefault();
                    $.ajax({
                        type: 'POST',
                        contentType: 'application/json',
                        url: 'set-product',
                        dataType : 'json',
                        data : JSON.stringify({"delete_product": true, "product_id": products_obj[$(this).attr("id")]}),
                        success : function (result) {
                            console.log(result);
                        }, error : function (result) {
                            console.log(result);
                        }   
                    });
                });

            } else {
                alert("Error in received data.");
            }
        });
    });

    $("a#repository").click(function (event) {
        event.preventDefault();
        $.post("repository-api", function (response, status) {
            data_div_cleaner();
            if (status == "success") {
                var header = "<h2>مدیریت انبارها</h2>";
                header += "<div>";
                header += '<a href="" class="btn_a" id="add_repository_btn">افزودن انبار</a> ';
                header += "</div>";

                var column_names = response.column_names;
                var table = '<table class="repositories_table">';
                table += "<tr>";
                table += "<th>" + "نام انبار" + "</th>";
                table += "<th>" + " " + "</th>";
                table += "</tr>";

                var repositories_obj = {};
                response.data.forEach(function (element) {
                    table += "<tr>";
                    table += "<td>" + element[column_names[1]] + "</td>";
                    table += '<td><a href="" class="edit_repository" id="edit_repository_' + element[column_names[0]] + '">ویرایش</a> ';
                    repositories_obj['edit_repository_' + element[column_names[0]]] = element[column_names[0]];
                    table += '<a href="" class="delete_repository" id="delete_repository_' + element[column_names[0]] + '">حذف</a></td>';
                    repositories_obj['delete_repository_' + element[column_names[0]]] = element[column_names[0]];
                    table += "</tr>";
                });
                table += "</table>";

                $("div#header_div").append(header);
                $("div#table_div").append(table);
                
                $("a#add_repository_btn").click(function (event) {
                    event.preventDefault();
                    console.log("add_repository_btn");
                });
                
            } else {
                alert("Error in received data.");
            }
        });
    });

    $("a#inventory").click(function (event) {
        event.preventDefault();
        $.post("inventory-api", function (response, status) {
            data_div_cleaner();
            if (status == "success") {
                var header = "<h2>مدیریت موجودی و قیمت‌ها</h2>";
                header += "<div>";
                header += '<a href="" class="btn_a" id="add_inventory_btn">افزودن موجودی</a> ';
                header += "</div>";

                var column_names = response.column_names;
                var table = '<table>';
                table += "<tr>";
                table += "<th>" + "انبار" + "</th>";
                table += "<th>" + "کالا" + "</th>";
                table += "<th>" + "قیمت" + "</th>";
                table += "<th>" + "موجودی" + "</th>";
                table += "<th>" + " " + "</th>";
                table += "</tr>";

                var inventories_obj = {};
                response.data.forEach(function (element) {
                    table += "<tr>";
                    table += "<td>" + element[column_names[1]] + "</td>";
                    table += "<td>" + element[column_names[2]] + "</td>";
                    table += "<td>" + element[column_names[3]] + "</td>";
                    table += "<td>" + element[column_names[4]] + "</td>";
                    table += '<td><a href="" class="edit_inventory" id="edit_inventory_' + element[column_names[0]] + '">ویرایش</a> ';
                    inventories_obj['edit_inventory_' + element[column_names[0]]] = element[column_names[0]];
                    table += '<a href="" class="delete_inventory" id="delete_inventory_' + element[column_names[0]] + '">حذف</a></td>';
                    inventories_obj['delete_inventory_' + element[column_names[0]]] = element[column_names[0]];
                    table += "</tr>";
                });
                table += "</table>";

                $("div#header_div").append(header);
                $("div#table_div").append(table);
                
                $("a#add_inventory_btn").click(function (event) {
                    event.preventDefault();
                    console.log("add_inventory_btn");
                });
                
            } else {
                alert("Error in received data.");
            }
        });
    });

    $("a#order").click(function (event) {
        event.preventDefault();
        $.post("order-api", function (response, status) {
            data_div_cleaner();
            if (status == "success") {
                var header = "<h2>مدیریت سفارش‌ها</h2>";

                var column_names = response.column_names;
                var table = '<table>';
                table += "<tr>";
                table += "<th>" + "نام کاربر" + "</th>";
                table += "<th>" + "مجموع مبلغ" + "</th>";
                table += "<th>" + "زمان ثبت سفارش" + "</th>";
                table += "<th>" + " " + "</th>";
                table += "</tr>";

                var orders_obj = {};
                response.data.forEach(function (element) {
                    table += "<tr>";
                    table += "<td>" + element[column_names[1]] + "</td>";
                    table += "<td>" + element[column_names[2]] + "</td>";
                    table += "<td>" + element[column_names[3]] + "</td>";
                    table += '<td><a href="" class="order_detail" id="order_detail_' + element[column_names[0]] + '">بررسی سفارش</a></td>';
                    orders_obj['order_detail_' + element[column_names[0]]] = element[column_names[0]];
                    table += "</tr>";
                });
                table += "</table>";

                $("div#header_div").append(header);
                $("div#table_div").append(table);
            } else {
                alert("Error in received data.");
            }
        });
    });

});
