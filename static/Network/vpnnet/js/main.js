class VPNNetPage {
    StoreKEY = 'VPNNetKey';
    constructor() {
        this.mask_box = document.querySelector('#mask-box');
        this.tbody = document.querySelector('#tbody');
        this.verify = document.querySelector('#verify');
        this.key_input = document.querySelector('#key');

        this.key = null;
        this.load_key();

        this.verify.addEventListener('click', () => {
            this.key = this.key_input.value;
            Store.save(this.StoreKEY, key);
            this.load_key();
        })
    }

    load_key() {
        this.key = Store.load(this.StoreKEY);
        console.log(this.key)
        if (this.key) {
            this.update();
        } else {
            activate(this.mask_box)
        }
    }

    update() {
        Request.get('/dev/api/network/vpnnet/session', {token: this.key})
            .then((data) => {
                deactivate(this.mask_box);
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
            .catch((err) => {
                Store.remove(this.StoreKEY)
                this.load_key();
            });
    }
}