
Date.prototype.subtractHours = function(h) {
  this.setTime(this.getTime() - (h*60*60*1000));
  return this;
}

function tim_benh_nhan(){
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
        console.info(res)
        return res.json()
    }).then(function(data){
        console.info(data)
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
            cell = row.insertCell()
            cell.innerHTML = `<a href="/them-dskham?id=${i.id}" >Thêm</a>`
        }
    })
}

function benh_nhan_info(){
    document.getElementById("benh_nhan").style.display = "none";
    document.getElementById("ds_kham").style.display = "none"
    document.getElementById("lich_duyet").style.display = "none"
    let table = document.getElementById("benh_nhan_info_form");
    table.style.display = "block";
}

function benh_nhan_click(){
    document.getElementById("benh_nhan_info_form").style.display = "none"
    document.getElementById("ds_kham").style.display = "none"
    document.getElementById("lich_duyet").style.display = "none"
    let table = document.getElementById("benh_nhan")
    table.style.display = "block"
}

function duyet_lich(){
    document.getElementById("benh_nhan_info_form").style.display = "none"
    document.getElementById("ds_kham").style.display = "none"
    document.getElementById("benh_nhan").style.display = "none"
    let table = document.getElementById("lich_duyet")
    table.style.display = "block"
    fetch("/api/ds-duyet-lich", {
            method: "get",
            headers: {
                "Content-Type": "application/json"
            }
        }).then(function(res){
            console.info(res)
            return res.json()
        }).then(function(data){
            console.info(data)
            let table = document.getElementById("bang_duyet_lich")
            table.innerHTML = ""
            for(i of data.danh_sach){
                let row = table.insertRow()
                let cell = row.insertCell()
                cell.innerText = i.id;
                cell = row.insertCell()
                cell.innerText = i.ten
                cell = row.insertCell()
                cell.innerText = toLocalDateString(i.ngay_dk_kham)
                cell = row.insertCell()
                cell.innerText = i.so_dt
                cell = row.insertCell()
                cell.innerHTML = `<a href="javascript:;" onclick="duyet_benh_nhan(${i.id_dk}, '${formatInsertDate(i.ngay_dk_kham)}', ${i.id})">Duyệt</a> | <a href="javascript:;" onclick="tu_choi_benh_nhan(${i.id_dk})">Từ chối</a>`
            }
        })
}

function duyet_benh_nhan(id_dk, ngay_dk_kham, id_benh_nhan){
    if (confirm("Bạn có chắc duyệt người này không?") == true)
    xoa_luu_tam_thoi(id_dk)
    them_ds_kham(ngay_dk_kham, id_benh_nhan)
    alert('Duyệt thành công')
    fetch("/api/gui_sms",{
        method: "post",
        body: JSON.stringify({
            "SDT": "0964147757",
            "message": "Đăng ký của bạn đã được duyệt"
        }),
        headers: {
                "Content-Type": "application/json"
        }
    }).then(function(res){
        return res.json()
    }).then(function(data){

    })
    location.reload()
}

async function xoa_luu_tam_thoi(id){
        await fetch("/api/delete-luu-tam-thoi/" + id, {
        method: "delete"
        }).then(function(res) {
            console.log(res)
            return res.json()
        }).then(function(data) {
            console.log(data)
        })
}

async function tu_choi_benh_nhan(id_dk){
    if (confirm("Bạn có chắc muốn từ chối người này không?") == true)
    await xoa_luu_tam_thoi(id_dk)
    xoa_dk_onl(id_dk)
    alert('Từ chối thành công')
    fetch("/api/gui_sms",{
        method: "post",
        body: JSON.stringify({
            "SDT": "0964147757",
            "message": "Rất tiếc đăng ký bạn không được duyệt"
        }),
        headers: {
                "Content-Type": "application/json"
        }
    }).then(function(res){
        return res.json()
    }).then(function(data){

    })
    location.reload()
}

function xoa_dk_onl(id){
    fetch("/api/delete-dk-onl/" + id, {
            method: "delete"
            }).then(function(res) {
                console.log(res)
                return res.json()
            }).then(function(data) {
                console.log(data)
            })
}



function them_ds_kham(ngay_kham_dk, id_benh_nhan) {
    fetch("/api/them-ds-kham", {
        method: 'post',
        body: JSON.stringify({
            "id_benh_nhan": id_benh_nhan,
            "ngay_kham_dk": ngay_kham_dk
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)
    })
}



function ds_kham_click(){
   document.getElementById("benh_nhan").style.display = "none";
   document.getElementById("benh_nhan_info_form").style.display = "none"
   document.getElementById("lich_duyet").style.display = "none"
   let table = document.getElementById("ds_kham");
   table.style.display = "block";
}

function xem_ds_kham(){
    let date = document.getElementById("day").value
    fetch("api/xem-dskham" + "/" + date, {
            method: "get",
            headers: {
                "Content-Type": "application/json"
            }
        }).then(function(res){
            console.info(res)
            return res.json()
        }).then(function(data){
            console.info(data)
            let table = document.getElementById("ds_kham_table")
            table.innerHTML = ""
            let stt = 1;
            for(i of data.danh_sach){
                let row = table.insertRow()
                let cell = row.insertCell()
                cell.innerText = stt++;
                cell = row.insertCell()
                cell.innerText = i.ten
                cell = row.insertCell()
                cell.innerText = i.SDT
                cell = row.insertCell()
                cell.innerText = toLocalDateString(i.ngay_kham)
            }
        })
}

function toDateString(dateString){
    let date = new Date(dateString)
    return date.getDate() + "/" + (date.getMonth()+1) + "/" + date.getFullYear()
}

function toLocalDateString(dateString){
    let date = new Date(dateString).subtractHours(7)
    return date.getDate() + "/" + (date.getMonth()+1) + "/" + date.getFullYear()
}

function formatInsertDate(dateString){
     let date = new Date(dateString).subtractHours(7)
     return date.getFullYear() + "-" + (date.getMonth()+1) + "-" + date.getDate() + " " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds()
}