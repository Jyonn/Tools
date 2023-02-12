class VPNNetPage {
    constructor() {
        this.mask_box = document.querySelector('#mask-box');
        this.tbody = document.querySelector('#tbody');
        this.verify = document.querySelector('#verify');
        this.key_input = document.querySelector('#key');

        this.key = Store.load('VPNNetKey');
        if (this.key) {
            deactivate(this.mask_box)
            this.update();
        } else {
            activate(this.mask_box)
        }

        this.verify.addEventListener('click', () => {
            let key = this.key_input.value;
            Store.save('VPNNetKey', key);
            deactivate(this.mask_box);
            this.update();
        })
    }

    update() {
        Request.get('https://tools.6-79.cn/dev/api/network/vpnnet/session', {token: this.key})
            .then((data) => {
                console.log(data);
                this.tbody.innerHTML = '';
                data.forEach((item) => {
                    let tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${item.date}</td>
                        <td>${item.start}</td>
                        <td>${item.end}</td>
                        <td>${item.start_download}</td>
                        <td>${item.download}</td>
                    `;
                    this.tbody.appendChild(tr);
                })
            })
    }
}