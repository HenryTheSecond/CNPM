function tim_thuoc(){
    let kw = document.getElementsByName("kw")[0].value
    fetch("api/tim-thuoc?kw=" + kw, {
        method: "get",
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res){
        return res.json()
    }).then(function(data){
        let table = document.getElementById("thuoc_table")
        table.innerHTML = ""
        for(i of data.danh_sach){
            let row = table.insertRow()
            let cell = row.insertCell()
            cell.innerText = i.id
            cell = row.insertCell()
            cell.innerText = i.ten_thuoc
            cell = row.insertCell()
            cell.innerText = i.don_vi
            cell = row.insertCell()
            cell.innerText = i.gia
            cell = row.insertCell()
            cell.innerText = i.so_luong
        }
    })
}

function tim_benh_nhan(){
    document.getElementById("lich_su_kham_benh").style.display = "none"
    var loai_tim_kiem = document.querySelector('input[name="tim_kiem_benh_nhan"]:checked').id;
    var kw
    if(loai_tim_kiem == "tim_kiem_theo_ngay")
        kw = document.getElementById("ngay_tim_kiem").value
    else
        kw = document.getElementsByName("tim_kiem_kw")[0].value
    fetch("api/tim-benh-nhan?type=" + loai_tim_kiem + "&kw=" + kw,{
        method: "get",
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res){
        return res.json()
    }).then(function(data){
        let table = document.getElementById("benh_nhan_table")
        table.innerHTML = ""
        for(i of data.danh_sach){
            let row = table.insertRow()
            let cell = row.insertCell()
            cell.innerText = i.id
            cell = row.insertCell()
            cell.innerText = i.ten
            cell = row.insertCell()
            cell.innerText = i.gioi_tinh
            cell = row.insertCell()
            cell.innerText = i.dia_chi
            cell = row.insertCell()
            cell.innerText = toDateString(i.ngay_sinh)
            cell = row.insertCell()
            cell.innerText = i.SDT
            row.onclick = function(){
                document.getElementById("lich_su_kham_benh").style.display = "block"
                fetch("api/lich-su-kham-benh?id=" + row.cells[0].innerText,{
                    method : "get",
                    headers: {
                        "Content-Type": "application/json"
                    }
                }).then(function(result){
                    return result.json()
                }).then(function(d){
                    let table = document.getElementById("lich_su_kham_benh_data")
                    table.innerHTML = ""
                    for(i of d.danh_sach){
                        let row = table.insertRow()
                        let cell = row.insertCell()
                        cell.innerText = i.id
                        cell = row.insertCell()
                        cell.innerText = i.ngay_kham
                        cell = row.insertCell()
                        cell.innerText = i.trieu_chung
                        cell = row.insertCell()
                        cell.innerText = i.benh
                        cell = row.insertCell()
                        cell.innerText = i.bac_si
                        cell = row.insertCell()
                        for(j of i.don_thuoc){
                            cell.innerText += "Thuốc: " + j.ten + "     Số lượng: " + j.so_luong + "    Cách dùng: " + j.cach_dung + "\n"
                        }
                    }
                })
            };
        }
    })
}

function lap_phieu_tim_benh_nhan(){
    var kw = document.getElementsByName("tim_kiem_kw")[1].value
    fetch("api/tim-benh-nhan-kham-benh?" + "&kw=" + kw,{
        method: "get",
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res){
        return res.json()
    }).then(function(data){
        let table = document.getElementById("tim_kiem_lap_phieu_kham_benh")
        table.innerHTML = ""
        for(i of data.danh_sach){
            let row = table.insertRow()
            let cell = row.insertCell()
            cell.innerText = i.id_kham_benh
            cell = row.insertCell()
            cell.innerText = i.id
            cell = row.insertCell()
            cell.innerText = i.ten
            cell = row.insertCell()
            cell.innerText = i.gioi_tinh
            cell = row.insertCell()
            cell.innerText = i.dia_chi
            cell = row.insertCell()
            cell.innerText = toDateString(i.ngay_sinh)
            cell = row.insertCell()
            cell.innerText = i.SDT
            row.onclick = function(){
                document.getElementById("id").value = row.cells[0].innerText
            };
        }
    })
}

function them_thuoc_click(thuoc, cach_dung){
    let clone = document.getElementsByName("don_thuoc")[0].cloneNode( true );
    document.getElementById("don_thuoc").appendChild(clone)
    console.log(clone)
}

function xoa_thuoc_click(){
    let index = document.getElementsByName("don_thuoc").length - 1
    if(index>0){
        let obj = document.getElementsByName("don_thuoc")[index]
        obj.remove()
    }
}

function toDateString(dateString){
    let date = new Date(dateString)
    return date.getDate() + "/" + (date.getMonth()+1) + "/" + date.getFullYear()
}