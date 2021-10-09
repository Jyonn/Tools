class FotoPage {
    constructor() {
        this.albums = []
        this.fotos = []
        this.fotos = []

        this.currentAlbum = null
        this.albumBox = getByClass('album-box')
        this.fotoBox = getByClass('foto-box')
        this.fileInput = getByClass('file-input')
        this.buttonBox = getByClass('button-box')
        this.removeButton = getById('remove')
        this.removeActive = false
        this.pinButton = getById('pin')
        this.pinActive = false

        this.fileInput.addEventListener('change', this.uploadFiles.bind(this))
        this.uploadFileList = []
    }

    activateRemoveMode() {
        this.removeActive = true
        activate(this.removeButton)
        this.fotoBox.classList.add('remove-mode')
        this.deactivatePinMode()
    }

    deactivateRemoveMode() {
        this.removeActive = false
        deactivate(this.removeButton)
        this.fotoBox.classList.remove('remove-mode')
    }

    activatePinMode() {
        this.pinActive = true
        activate(this.pinButton)
        this.fotoBox.classList.add('pin-mode')
        this.deactivateRemoveMode()
    }

    deactivatePinMode() {
        this.pinActive = false
        deactivate(this.pinButton)
        this.fotoBox.classList.remove('pin-mode')
    }

    toggleRemoveMode() {
        if (this.removeActive) {
            this.deactivateRemoveMode()
        } else {
            this.activateRemoveMode()
        }
    }

    togglePinMode() {
        if (this.pinActive) {
            this.deactivatePinMode()
        } else {
            this.activatePinMode()
        }
    }

    showUploadBox() {
        activate(this.fotoBox)
        activate(this.buttonBox)
    }

    hideUploadBox() {
        deactivate(this.fotoBox)
        deactivate(this.buttonBox)
    }

    getToken() {
        Request.saveToken(prompt('Admin Token'))
    }

    initAlbumBox() {
        let albumTemplate = template`<div class="album" onclick="fotoPage.fetchAlbum('${0}')">${0}</div>`
        let selectedAlbumTemplate = template`<div class="album selected" onclick="fotoPage.fetchAlbum('${0}')">${0}</div>`

        this.albumBox.innerHTML = ''

        for (let album of this.albums) {
            if (album === this.currentAlbum) {
                this.albumBox.appendChild(stringToHtml(selectedAlbumTemplate(album)))
            }
            else {
                this.albumBox.appendChild(stringToHtml(albumTemplate(album)))
            }
        }
    }

    removeUploading(index) {
        let l = this.uploadFileList.slice(0, index)
        let r = this.uploadFileList.slice(index + 1)
        this.uploadFileList = l.concat(r)
        this.initFotoBox()
    }

    initFotoBox() {
        let fotoTemplate = template`<div class="foto img-fit" style="background-image: url('${0}')" onclick="fotoPage.clickFoto('${1}')"></div>`
        let fotoUploadingTemplate = template`<div class="foto img-fit uploading" style="background-image: url('${0}')" onclick="fotoPage.removeUploading(${1})"></div>`
        let fotoUploadedTemplate = template`<div class="foto img-fit uploaded" style="background-image: url('${0}')"></div>`
        this.fotoBox.innerHTML = ''

        for (let i = 0; i < this.uploadFileList.length; i++) {
            let file = this.uploadFileList[i].file
            let uploaded = this.uploadFileList[i].uploaded
            let url = window.URL.createObjectURL(file)
            if (uploaded) {
                this.fotoBox.appendChild(stringToHtml(fotoUploadedTemplate(url)))
            } else {
                this.fotoBox.appendChild(stringToHtml(fotoUploadingTemplate(url, i)))
            }
        }

        for (let foto of this.fotos) {
            this.fotoBox.appendChild(stringToHtml(fotoTemplate(foto.sources.square, foto.foto_id)))
        }
    }

    clickFoto(foto_id) {
        if (this.removeActive) {
            Request.delete('https://tools.6-79.cn/dev/api/arts/foto/' + foto_id).then(_ => {
                this.fetchAlbum(this.currentAlbum)
            })
        }
    }

    fetchHomePage() {
        this.currentAlbum = null

        Request.get('https://tools.6-79.cn/dev/api/arts/foto/')
            .then(data => {
                this.albums = []
                data.albums.forEach(album => this.albums.push(album.name))
                this.fotos = data.fotos
                this.initAlbumBox()
                this.hideUploadBox()
                this.initFotoBox()
            }).catch(ErrorHandler.handler)
    }

    fetchAlbum(album) {
        this.currentAlbum = album

        this.initAlbumBox()
        Request.get('https://tools.6-79.cn/dev/api/arts/foto/album/' + album)
            .then(data => {
                this.fotos = data.fotos
                this.showUploadBox()
                this.initFotoBox()
            }).catch(ErrorHandler.handler)
    }

    fetchUploadTokens() {
        let count = this.uploadFileList.length
        Request.get('https://tools.6-79.cn/dev/api/arts/foto/token', {
            image_num: count,
            album: this.currentAlbum
        }).then(data => {
            for (let i = 0; i < data.length; i++) {
                if (this.uploadFileList[i].uploaded) {
                    continue
                }
                let token = data[i][0], key = data[i][1]
                let file = this.uploadFileList[i].file
                let fd = new FormData()
                fd.append('key', key)
                fd.append('token', token)
                fd.append('file', file)

                Request.post('https://up.qiniup.com/', fd, false, false)
                    .then(_ => {
                        this.uploadFileList[i].uploaded = true
                        this.initFotoBox()
                    })
                this.clearUploadFiles()
                this.fetchAlbum(this.currentAlbum)
            }
        })
    }

    newAlbum() {
        let album = prompt('Album Name')
        if (!album) {
            return
        }

        Request.post('https://tools.6-79.cn/dev/api/arts/foto/album/' + album)
            .then(_ => {
                this.fetchHomePage()
            })
    }

    clearUploadFiles() {
        this.uploadFileList = []
        this.initFotoBox()
    }

    confirmUploadFiles() {
        if (confirm('Confirm Upload?')) {
            this.fetchUploadTokens()
        }
    }

    uploadFiles() {
        if (!this.fileInput.files) {
            return
        }

        this.showUploadBox()
        for (let file of this.fileInput.files) {
            this.uploadFileList.push({uploaded: false, file})
        }

        this.initFotoBox()
    }
}