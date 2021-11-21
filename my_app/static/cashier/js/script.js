function bao_cao_doanh_thu_click(){
    document.getElementById("benh_nhan_da_lap_phieu").style.display = "none"
    let table = document.getElementById("doanh_thu_info");
    table.style.display = "block";
}


function lap_hoa_don_click(){
    document.getElementById("doanh_thu_info").style.display = "none"
    let table = document.getElementById("benh_nhan_da_lap_phieu");
    table.style.display = "block";
    fetch("api/xem-ds-phieu", {
            method: "get",
            headers: {
                "Content-Type": "application/json"
            }
        }).then(function(res){
            console.info(res)
            return res.json()
        }).then(function(data){
            console.info(data)
            let table = document.getElementById("benh_nhan_da_lap_phieu_table")
            table.innerHTML = ""
            for(i of data.danh_sach){
                let row = table.insertRow()
                let cell = row.insertCell()
                cell.innerText = i.kham_benh_id
                cell = row.insertCell()
                cell.innerText = i.ten_benh_nhan
                cell = row.insertCell()
                cell.innerText = i.trieu_chung
                cell = row.insertCell()
                cell.innerText = i.ten_benh
                cell = row.insertCell()
                cell.innerText = toDateString(i.ngay_kham)
                cell = row.insertCell()
                cell.innerHTML = `<a href="#" >Chọn</a>`
            }
        })
}


