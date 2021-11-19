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