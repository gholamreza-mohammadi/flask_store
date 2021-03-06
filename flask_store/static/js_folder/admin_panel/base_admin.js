
function data_div_cleaner() {
    // console.log("data_div_cleaner");
    $("div#header_div").empty();
    $("div#table_div").empty();
}

$(function () {

    $("a#product").click(function (event) {
        event.preventDefault();
        function load_product_table() {
            // console.log("load_product_table");
            $.post("get-products", function (response, status) {
                data_div_cleaner();
                if (status == "success") {
                    var header = '<div class="w-75 mx-auto d-flex justify-content-between">';
                    header += "<h2>مدیریت کالاها</h2>";
                    header += "<div>";
                    header += '<a href="" class="btn btn-success" id="add_products_btn">import</a> ';
                    header += '<a href="" class="btn btn-success" id="add_product_btn">افزودن کالا</a>';
                    header += "</div>";
                    header += "</div>";

                    var column_names = response.column_names;
                    var table = '<table class="w-75 mx-auto table table-striped table-bordered">';
                    table += '<tr class="table-dark">';
                    table += "<th>" + "تصویر" + "</th>";
                    table += "<th>" + "نام کالا" + "</th>";
                    table += "<th>" + "دسته بندی" + "</th>";
                    table += '<th class="text-center">' + "ویرایش / حذف" + "</th>";
                    table += "</tr>";

                    var products_obj = {};
                    response.data.forEach(function (element) {
                        table += "<tr>";
                        table += '<td class="text-center"><a href=' + element[column_names[1]] + " target='_blank'>link</a></td>";
                        table += "<td>" + element[column_names[2]] + "</td>";
                        table += "<td>" + element[column_names[3]] + "</td>";
                        table += '<td class="text-center"><a href="" class="edit_product btn btn-secondary" id="edit_product_' + element[column_names[0]] + '">ویرایش</a> ';
                        products_obj['edit_product_' + element[column_names[0]]] = {
                            'id': element[column_names[0]],
                            'image_link': element[column_names[1]],
                            'name': element[column_names[2]],
                            'category': element[column_names[3]],
                            'description': element[column_names[4]]
                        };

                        table += '<a href="" class="delete_product btn btn-danger" id="delete_product_' + element[column_names[0]] + '">حذف</a></td>';
                        products_obj['delete_product_' + element[column_names[0]]] = element[column_names[0]];
                        table += "</tr>";
                    });
                    table += "</table>";

                    $("div#header_div").append(header);
                    $("div#table_div").append(table);

                    $("a#add_product_btn").click(function (event) {
                        event.preventDefault();
                        $.post("get-category", function (response, status) {
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
                                popup += "<h4>لینک تصویر:</h4>";
                                popup += '<input type="text" class="product_image_link" id="product_image_link" name="product_image_link"><br>';
                                popup += "<h4>توضیحات کالا:</h4>";
                                popup += '<textarea id="product_description" name="product_description" rows="5" wrap="soft"></textarea><br>';
                                popup += '<div class="container"><a href="" class="btn btn-success" id="save_product_btn">ذخیره</a></div>';
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
                                                                   "product_image_link": $('input#product_image_link').val(),
                                                                   "product_name": $('input#product_name').val(),
                                                                   "product_category": $('select#product_category').find(":selected").text(),
                                                                   "product_description": $('textarea#product_description').val()})   
                                        }).always(load_product_table);
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
                        popup += "<h4>انتخاب فایل:</h4>";
                        popup += '<form method="POST" enctype="multipart/form-data" id="fileUploadForm">';
                        popup += '<div dir="ltr"><input dir="ltr" id="products_file" name="products_file" type="file"></div>';
                        popup += '<div class="container"><button type="submit" class="btn btn-success">آپلود و ذخیره‌سازی جدول</button></div></form>';
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
                                }).always(load_product_table);
                                $("div.popup").trigger('close');
                            }
                        });
                    });

                    $("a.edit_product").click(function (event) {
                        event.preventDefault();
                        var product_obj = products_obj[$(this).attr("id")];
                        $.post("get-category", function (response, status) {
                            if (status == "success") {
                                var popup = '<div class="popup">';
                                popup += "<h2>افزودن / ویرایش کالا</h2>";
                                popup += "<h4>نام کالا:</h4>";
                                popup += '<input type="text" id="edit_product_name" name="edit_product_name" value="' + product_obj.name + '"><br>';
                                popup += "<h4>دسته بندی:</h4>";
                                popup += '<select name="edit_product_category" id="edit_product_category">';
                                response.data.forEach(function (element) {
                                    if (element == product_obj.category) {
                                        popup += "<option value=" + element + " selected>" + element + "</option>";
                                    } else {
                                        popup += "<option value=" + element + ">" + element + "</option>";
                                    }
                                });
                                popup += "</select><br>";
                                popup += "<h4>لینک تصویر:</h4>";
                                popup += '<input type="text" class="product_image_link" id="edit_product_image_link" name="edit_product_image_link" value="' + product_obj.image_link + '"><br>';
                                popup += "<h4>توضیحات کالا:</h4>";
                                popup += '<textarea id="edit_product_description" name="edit_product_description" rows="5" wrap="soft">' + product_obj.description + '</textarea><br>';
                                popup += '<div class="container"><a href="" class="btn btn-success" id="save_edited_product_btn">ذخیره</a></div>';
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
                                                                   "product_id": product_obj.id,
                                                                   "product_image_link": $('input#edit_product_image_link').val(),
                                                                   "product_name": $('input#edit_product_name').val(),
                                                                   "product_category": $('select#edit_product_category').find(":selected").text(),
                                                                   "product_description": $('textarea#edit_product_description').val()})  
                                        }).always(load_product_table);
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
                        var product_obj = products_obj[$(this).attr("id")];
                        $.ajax({
                            type: 'POST',
                            contentType: 'application/json',
                            url: 'set-product',
                            dataType : 'json',
                            data : JSON.stringify({"delete_product": true, "product_id": product_obj})   
                        }).always(load_product_table);
                    });

                } else {
                    alert("Error in received data.");
                }
            });
        }
        load_product_table();
    });

    $("a#repository").click(function (event) {
        event.preventDefault();
        function load_repository_table() {
            // console.log("load_repository_table");
            $.post("get-repository", function (response, status) {
                data_div_cleaner();
                if (status == "success") {
                    var header = '<div class="w-50 mx-auto d-flex justify-content-between">';
                    header += "<h2>مدیریت انبارها</h2>";
                    header += '<div><a href="" class="btn btn-success" id="add_repository_btn">افزودن انبار</a></div>';
                    header += "</div>";

                    var column_names = response.column_names;
                    var table = '<table class="w-50 mx-auto table table-striped table-bordered">';
                    table += '<tr class="table-dark">';
                    table += "<th>" + "نام انبار" + "</th>";
                    table += '<th class="text-center">' + "ویرایش / حذف" + "</th>";
                    table += "</tr>";

                    var repositories_obj = {};
                    response.data.forEach(function (element) {
                        table += "<tr>";
                        table += "<td>" + element[column_names[1]] + "</td>";
                        table += '<td class="text-center"><a href="" class="edit_repository btn btn-secondary" id="edit_repository_' + element[column_names[0]] + '">ویرایش</a> ';
                        repositories_obj['edit_repository_' + element[column_names[0]]] = {
                            'id': element[column_names[0]],
                            'name': element[column_names[1]]
                        };
                        table += '<a href="" class="delete_repository btn btn-danger" id="delete_repository_' + element[column_names[0]] + '">حذف</a></td>';
                        repositories_obj['delete_repository_' + element[column_names[0]]] = element[column_names[0]];
                        table += "</tr>";
                    });
                    table += "</table>";

                    $("div#header_div").append(header);
                    $("div#table_div").append(table);
                    
                    $("a#add_repository_btn").click(function (event) {
                        event.preventDefault();
                        var popup = '<div class="popup">';
                        popup += "<h2>افزودن / ویرایش انبار:</h2>";
                        popup += "<h4>نام انبار:</h4>";
                        popup += '<input type="text" id="repository_name" name="repository_name"><br>';
                        popup += '<div class="container"><a href="" class="btn btn-success" id="save_repository_btn">ذخیره</a></div>';
                        popup += "</div>";

                        $("div#popup_div").append(popup);
                        $("div.popup").lightbox_me();

                        $("a#save_repository_btn").click(function (event) {
                            event.preventDefault();
                            if ($('input#repository_name').val().length) {
                                $.ajax({
                                    type: 'POST',
                                    contentType: 'application/json',
                                    url: 'set-repository',
                                    dataType : 'json',
                                    data : JSON.stringify({"add_repository": true,
                                                           "repository_name": $('input#repository_name').val()})  
                                }).always(load_repository_table);
                                $("div.popup").trigger('close');
                            }
                        });

                    });

                    $("a.edit_repository").click(function (event) {
                        event.preventDefault();
                        var repository_obj = repositories_obj[$(this).attr("id")];
                        var popup = '<div class="popup">';
                        popup += "<h2>افزودن / ویرایش انبار:</h2>";
                        popup += "<h4>نام انبار:</h4>";
                        popup += '<input type="text" id="edit_repository_name" name="edit_repository_name" value="' + repository_obj.name + '"><br>';
                        popup += '<div class="container"><a href="" class="btn btn-success" id="save_repository_btn">ذخیره</a></div>';
                        popup += "</div>";

                        $("div#popup_div").append(popup);
                        $("div.popup").lightbox_me();

                        $("a#save_repository_btn").click(function (event) {
                            event.preventDefault();
                            if ($('input#edit_repository_name').val().length) {
                                $.ajax({
                                    type: 'POST',
                                    contentType: 'application/json',
                                    url: 'set-repository',
                                    dataType : 'json',
                                    data : JSON.stringify({"edit_repository": true,
                                                           "repository_id": repository_obj.id,
                                                           "repository_name": $('input#edit_repository_name').val()})   
                                }).always(load_repository_table);
                                $("div.popup").trigger('close');
                            }
                        });

                    });

                    $("a.delete_repository").click(function (event) {
                        event.preventDefault();
                        var repository_obj = repositories_obj[$(this).attr("id")];
                        $.ajax({
                            type: 'POST',
                            contentType: 'application/json',
                            url: 'set-repository',
                            dataType : 'json',
                            data : JSON.stringify({"delete_repository": true, "repository_id": repository_obj})
                        }).always(load_repository_table);
                    });
                    
                } else {
                    alert("Error in received data.");
                }
            });
        }
        load_repository_table();
    });

    $("a#inventory").click(function (event) {
        event.preventDefault();
        function load_inventory_table() {
            // console.log("load_inventory_table");
            $.post("get-inventory", function (response, status) {
                data_div_cleaner();
                if (status == "success") {
                    var header = '<div class="w-75 mx-auto d-flex justify-content-between">';
                    header += "<h2>مدیریت موجودی و قیمت‌ها</h2>";
                    header += "<div>";
                    header += '<a href="" class="btn btn-success" id="add_inventory_btn">افزودن موجودی</a> ';
                    header += "</div>";
                    header += "</div>";

                    var column_names = response.column_names;
                    var table = '<table class="w-75 mx-auto table table-striped table-bordered">';
                    table += '<tr class="table-dark">';
                    table += "<th>" + "انبار" + "</th>";
                    table += "<th>" + "کالا" + "</th>";
                    table += "<th>" + "قیمت" + "</th>";
                    table += "<th>" + "موجودی" + "</th>";
                    table += '<th class="text-center">' + "ویرایش / حذف" + "</th>";
                    table += "</tr>";

                    var inventories_obj = {};
                    response.data.forEach(function (element) {
                        table += "<tr>";
                        table += "<td>" + element[column_names[1]] + "</td>";
                        table += "<td>" + element[column_names[2]] + "</td>";
                        table += "<td>" + element[column_names[3]] + "</td>";
                        table += "<td>" + element[column_names[4]] + "</td>";
                        table += '<td class="text-center"><a href="" class="edit_inventory btn btn-secondary" id="edit_inventory_' + element[column_names[0]] + '">ویرایش</a> ';
                        inventories_obj['edit_inventory_' + element[column_names[0]]] = {
                            'id': element[column_names[0]],
                            'repository': element[column_names[1]],
                            'commodity': element[column_names[2]],
                            'price': element[column_names[3]],
                            'quantity': element[column_names[4]]
                        };
                        table += '<a href="" class="delete_inventory  btn btn-danger" id="delete_inventory_' + element[column_names[0]] + '">حذف</a></td>';
                        inventories_obj['delete_inventory_' + element[column_names[0]]] = element[column_names[0]];
                        table += "</tr>";
                    });
                    table += "</table>";

                    $("div#header_div").append(header);
                    $("div#table_div").append(table);
                    
                    $("a#add_inventory_btn").click(function (event) {
                        event.preventDefault();
                        $.post("get-repository", function (response, status) {
                            if (status == "success") {
                                var repositories = response.data;
                                $.post("get-products", function (response, status) {
                                    if (status == "success") {
                                        var products = response.data;
                                        var product_names = response.data.map(input => input.commodity_name);
                                        var popup = '<div class="popup">';
                                        popup += "<h2>افزودن / ویرایش موجودی:</h2>";
                                        popup += "<h4>نام انبار:</h4>";
                                        popup += '<select name="inventory_repository" id="inventory_repository">';
                                        repositories.forEach(function (element) {
                                            popup += "<option value=" + element['repository_name'] + ">" + element['repository_name'] + "</option>";
                                        });
                                        popup += "</select><br>";
                                        popup += "<h4>نام کالا:</h4>";
                                        popup += '<input list="datalist_products" type="text" id="inventory_product_name" name="inventory_product_name"><br>'; 
                                        popup += '<datalist id="datalist_products">';
                                        product_names.forEach(function (element) {
                                            popup += '<option value="' + element + '">';
                                        });
                                        popup += '</datalist>';
                                        popup += "<h4>قیمت:</h4>";
                                        popup += '<input type="number" class="input_number" id="inventory_price" name="inventory_price" min="0"><br>';
                                        popup += "<h4>موجودی:</h4>";
                                        popup += '<input type="number" class="input_number" id="inventory_quantity" name="inventory_quantity" min="0"><br>';
                                        popup += '<div class="container"><a href="" class="btn btn-success" id="save_inventory_btn">ذخیره</a></div>';
                                        popup += "</div>";

                                        $("div#popup_div").append(popup);
                                        $("div.popup").lightbox_me();

                                        $("a#save_inventory_btn").click(function (event) {
                                            event.preventDefault();
                                            if (product_names.includes($('input#inventory_product_name').val()) * $('input#inventory_product_name').val().length * $('input#inventory_price').val().length * $('input#inventory_quantity').val().length) {
                                                $.ajax({
                                                    type: 'POST',
                                                    contentType: 'application/json',
                                                    url: 'set-inventory',
                                                    dataType : 'json',
                                                    data : JSON.stringify({"add_inventory": true,
                                                                           "inventory_product_id": products.find(element => element.commodity_name == $('input#inventory_product_name').val())._id,
                                                                           "inventory_repository_id": repositories.find(element => element.repository_name == $('select#inventory_repository').find(":selected").text())._id,
                                                                           "inventory_price": $('input#inventory_price').val(),
                                                                           "inventory_quantity": $('input#inventory_quantity').val()})  
                                                }).always(load_inventory_table);
                                                $("div.popup").trigger('close');
                                            } else {
                                                alert('ورودی نامناسب.'); // input name red color
                                            }
                                        });
                                    } else {
                                        alert("Error in received data.");
                                    }
                                });
                            } else {
                                alert("Error in received data.");
                            }
                        });
                    });
                    
                    $("a.edit_inventory").click(function (event) {
                        event.preventDefault();
                        var inventory_obj = inventories_obj[$(this).attr("id")];
                        $.post("get-repository", function (response, status) {
                            if (status == "success") {
                                var repositories = response.data;
                                $.post("get-products", function (response, status) {
                                    if (status == "success") {
                                        var products = response.data;
                                        var product_names = response.data.map(input => input.commodity_name);
                                        var popup = '<div class="popup">';
                                        popup += "<h2>افزودن / ویرایش موجودی:</h2>";
                                        popup += "<h4>نام انبار:</h4>";
                                        popup += '<select name="edit_inventory_repository" id="edit_inventory_repository">';
                                        repositories.forEach(function (element) {
                                            if (element['repository_name'] == inventory_obj.repository) {
                                                popup += "<option value=" + element['repository_name'] + " selected>" + element['repository_name'] + "</option>";
                                            } else {
                                                popup += "<option value=" + element['repository_name'] + ">" + element['repository_name'] + "</option>";
                                            }
                                        });
                                        popup += "</select><br>";
                                        popup += "<h4>نام کالا:</h4>";
                                        popup += '<input list="datalist_products" type="text" id="edit_inventory_product_name" name="edit_inventory_product_name" value="' + inventory_obj.commodity + '"><br>'; 
                                        popup += '<datalist id="datalist_products">';
                                        product_names.forEach(function (element) {
                                            popup += '<option value="' + element + '">';
                                        });
                                        popup += '</datalist>';
                                        popup += "<h4>قیمت:</h4>";
                                        popup += '<input type="number" class="input_number" id="inventory_price" name="inventory_price" min="0" value="' + inventory_obj.price + '"><br>';
                                        popup += "<h4>موجودی:</h4>";
                                        popup += '<input type="number" class="input_number" id="inventory_quantity" name="inventory_quantity" min="0" value="' + inventory_obj.quantity + '"><br>';
                                        popup += '<div class="container"><a href="" class="btn btn-success" id="save_inventory_btn">ذخیره</a></div>';
                                        popup += "</div>";

                                        $("div#popup_div").append(popup);
                                        $("div.popup").lightbox_me();

                                        $("a#save_inventory_btn").click(function (event) {
                                            event.preventDefault();
                                            if (product_names.includes($('input#edit_inventory_product_name').val()) * $('input#edit_inventory_product_name').val().length * $('input#inventory_price').val().length * $('input#inventory_quantity').val().length) {
                                                $.ajax({
                                                    type: 'POST',
                                                    contentType: 'application/json',
                                                    url: 'set-inventory',
                                                    dataType : 'json',
                                                    data : JSON.stringify({"edit_inventory": true,
                                                                           "inventory_id" : inventory_obj.id,
                                                                           "inventory_product_id": products.find(element => element.commodity_name == $('input#edit_inventory_product_name').val())._id,
                                                                           "inventory_repository_id": repositories.find(element => element.repository_name == $('select#edit_inventory_repository').find(":selected").text())._id,
                                                                           "inventory_price": $('input#inventory_price').val(),
                                                                           "inventory_quantity": $('input#inventory_quantity').val()})  
                                                }).always(load_inventory_table);
                                                $("div.popup").trigger('close');
                                            } else {
                                                alert('ورودی نامناسب.'); // input name red color
                                            }
                                        });
                                    } else {
                                        alert("Error in received data.");
                                    } });
                            } else {
                                alert("Error in received data.");
                            }
                        });
                    });

                    $("a.delete_inventory").click(function (event) {
                        event.preventDefault();
                        var inventory_obj = inventories_obj[$(this).attr("id")];
                        $.ajax({
                            type: 'POST',
                            contentType: 'application/json',
                            url: 'set-inventory',
                            dataType : 'json',
                            data : JSON.stringify({"delete_inventory": true, "inventory_id": inventory_obj})  
                        }).always(load_inventory_table);
                    });

                } else {
                    alert("Error in received data.");
                }
            });
        }
        load_inventory_table();
    });

    $("a#order").click(function (event) {
        event.preventDefault();
        $.post("get-order", function (response, status) {
            data_div_cleaner();
            if (status == "success") {
                var header = '<div class="w-75 mx-auto d-flex justify-content-between">';
                header += "<h2>مدیریت سفارش‌ها</h2>";
                header += "<div>";
                header += '<p> </p> ';
                header += "</div>";
                header += "</div>";

                var column_names = response.column_names;
                var table = '<table class="w-75 mx-auto table table-striped table-bordered">';
                table += '<tr class="table-dark">';
                table += "<th>" + "نام کاربر" + "</th>";
                table += "<th>" + "مجموع مبلغ" + "</th>";
                table += "<th>" + "زمان ثبت سفارش" + "</th>";
                table += '<th class="text-center">' + " " + "</th>";
                table += "</tr>";

                var orders_obj = {};
                response.data.forEach(function (element) {
                    table += "<tr>";
                    table += "<td>" + element[column_names[1]] + "</td>";
                    table += "<td>" + element[column_names[2]] + "</td>";
                    table += "<td>" + element[column_names[3]] + "</td>";

                    table += '<td class="text-center"><a href="" class="order_detail btn btn-secondary" id="order_detail_' + element[column_names[0]] + '">بررسی سفارش</a></td>';
                    orders_obj['order_detail_' + element[column_names[0]]] = {
                        'id': element[column_names[0]]
                    };
                    table += "</tr>";
                });
                table += "</table>";

                $("div#header_div").append(header);
                $("div#table_div").append(table);

                $("a.order_detail").click(function (event) {
                    event.preventDefault();
                    var order_obj = orders_obj[$(this).attr("id")];
                    $.ajax({
                        type: 'POST',
                        contentType: 'application/json',
                        url: 'get-order-detail',
                        dataType : 'json',
                        data : JSON.stringify({"order_detail": true,
                                               "order_id": order_obj.id})  
                    }).done(function (data) {
                        var popup = '<div class="popup order_div">';
                            popup += "<h4>نمایش سفارش</h4>";
                            popup += '<div class="my_table_div">';
                                popup += '<div class="table_div_row">';
                                    popup += '<div class="table_div_col">نام مشتری:</div>';
                                    popup += '<div class="table_div_col">' + data.user_name + '</div>';
                                popup += '</div>';
                                popup += '<div class="table_div_row">';
                                    popup += '<div class="table_div_col">آدرس:</div>';
                                    popup += '<div class="table_div_col">' + data.address + '</div>';
                                popup += '</div>';
                                popup += '<div class="table_div_row">';
                                    popup += '<div class="table_div_col">تلفن:</div>';
                                    popup += '<div class="table_div_col">' + data.phone + '</div>';
                                popup += '</div>';
                                popup += '<div class="table_div_row">';
                                    popup += '<div class="table_div_col">زمان تحویل:</div>';
                                    popup += '<div class="table_div_col">' + data.resive_time + '</div>';
                                popup += '</div>';
                                popup += '<div class="table_div_row">';
                                    popup += '<div class="table_div_col">زمان سفارش:</div>';
                                    popup += '<div class="table_div_col">' + data.order_time + '</div>';
                                popup += '</div>';
                            popup += '</div>';
                            popup += '<table class="table table-striped">';
                                popup += '<tr class="table-dark">';
                                    popup += "<th>" + "کالا" + "</th>";
                                    popup += "<th>" + "قیمت" + "</th>";
                                    popup += "<th>" + "انبار" + "</th>";
                                    popup += "<th>" + "تعداد" + "</th>";
                                popup += "</tr>";
                                data.products.forEach(function (product) {
                                    popup += "<tr>";
                                        popup += "<td>" + product.commodity_name + "</td>";
                                        popup += "<td>" + product.price + "</td>";
                                        popup += "<td>" + product.repository_name + "</td>";
                                        popup += "<td>" + product.quantity + "</td>";
                                    popup += "</tr>";
                                })
                            popup += "</table>";
                            popup += '<button id="close_btn" class="btn btn-secondary">بستن</button>';
                        popup += "</div>";

                        $("div#popup_div").append(popup);
                        $("div.popup").lightbox_me();
                        
                        $("button#close_btn").click(function (event) {
                            event.preventDefault();
                            $("div.popup").trigger('close');
                        });
                    });   
                });

            } else {
                alert("Error in received data.");
            }
        });
    });

});
