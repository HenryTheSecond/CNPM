function doanhThuNgay() {
    let date = document.getElementById("day").value
    fetch("/api/doanh-thu-ngay/" + date, {
        method: 'get',
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)

        let doanh_thu_ngay = document.getElementById("doanh-thu-ngay")
        doanh_thu_ngay.innerText = data.doanh_thu_ngay
    })
}