class FotoPage {
    constructor() {
        this.albums = []
        this.fotos = []
        this.base_url = 'https://tools.6-79.cn/dev/api/arts/foto'
        // this.base_url = 'http://localhost:8000/dev/api/arts/foto'

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

        Request.setHandler(this.requestHandler.bind(this))

        this.space = getQueryParam('space')
        if (!this.space) {
            alert('Please specify space')
        }
    }

    getToken() {
        Request.loadToken()
        if (!Request.token) {
            Request.saveToken(prompt('Admin Token'))
        }
    }

    requestHandler(resp) {
        if (resp.identifier === 'AUTH-ADMIN') {
            Request.saveToken(prompt('Admin Token'))
        } else {
            alert(resp.msg)
        }
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
        let fotoTemplate = template`<div class="foto img-fit ${2}" style="background-image: url('${0}')" onclick="fotoPage.clickFoto(this, '${1}')"></div>`
        let fotoUploadingTemplate = template`<div class="foto img-fit uploading" style="background-image: url('${0}')" onclick="fotoPage.removeUploading(${1})"></div>`
        let fotoUploadedTemplate = template`<div class="foto img-fit uploaded" style="background-image: url('${0}')"></div>`
        this.fotoBox.innerHTML = ''

        for (let i = 0; i < this.uploadFileList.length; i++) {
            let file = this.uploadFileList[i].file
            let uploaded = this.uploadFileList[i].uploaded
            let url = window.URL.createObjectURL(file)
            if (uploaded) {
                this.fotoBox.appendChild(stringToHtml(fotoUploadedTemplate(url)))
            } else {togglePinMode
                this.fotoBox.appendChild(stringToHtml(fotoUploadingTemplate(url, i)))
            }
        }

        let index = 0
        for (let foto of this.fotos) {
            this.fotoBox.appendChild(stringToHtml(fotoTemplate(foto.sources.square, index, foto.pinned ? 'foto-pinned' : '')))
            index += 1
        }
    }

    clickFoto(ele, index) {
        let foto = this.fotos[index]
        let foto_id = foto.foto_id

        if (this.removeActive) {
            Request.delete(this.base_url + '/' + foto_id).then(_ => {
                this.fetchAlbum(this.currentAlbum)
            })
        } else if (this.pinActive) {
            Request.put(this.base_url + '/' + foto_id).then(_ => {
                foto.pinned = !foto.pinned
                if (foto.pinned) {
                    ele.classList.add('foto-pinned')
                } else {
                    ele.classList.remove('foto-pinned')
                }
                this.initFotoBox()
            })
        }
    }

    fetchHomePage() {
        this.currentAlbum = null
        this.deactivatePinMode()
        this.deactivateRemoveMode()

        Request.get(this.base_url, {space: this.space})
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
        Request.get(this.base_url + '/album', {album: album, space: this.space})
            .then(data => {
                this.fotos = data.fotos
                this.showUploadBox()
                this.initFotoBox()
            }).catch(ErrorHandler.handler)
    }

    fetchUploadTokens() {
        let count = this.uploadFileList.length
        Request.get(this.base_url + '/token', {
            image_num: count,
            album: this.currentAlbum,
            space: this.space,
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

                let index = 0

                Request.post('https://up.qiniup.com/', fd, false, false)
                    .then(_ => {
                        this.uploadFileList[i].uploaded = true
                        this.initFotoBox()
                        index += 1
                    })

                let interval = setInterval(() => {
                    if (index === this.uploadFileList.length) {
                        this.clearUploadFiles()
                        clearInterval(interval)
                    }
                }, 500)
            }
        })
    }

    newAlbum() {
        let album = prompt('Album Name')
        if (!album) {
            return
        }

        Request.post(this.base_url + '/album', {album: album, space: this.space})
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

    renameAlbum() {
        let name = prompt('New Album Name', this.currentAlbum)
        if (name) {
            Request.put(this.base_url + '/album?album=' + this.currentAlbum + '&space=' + this.space, {name})
                .then(_ => {
                    this.fetchHomePage()
                })
        }
    }

    destroyAlbum() {
        if (confirm('Confirm Destroy Album?')) {
            Request.delete(this.base_url + '/album', {album: this.currentAlbum, space: this.space})
                .then(_ => {
                    this.fetchHomePage()
                })
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