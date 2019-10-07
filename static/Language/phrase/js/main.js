class PhrasePage {
    constructor() {
        this.entrance = getById('entrance');
        this.enter = getById('enter');
        this.loginMask = getById('login-mask');

        this.loadEntrance();
        this.enter.addEventListener('click', this.checkEntrance.bind(this));

        this.contributorSelectorTitle = getById('contributor-selector-title');
        this.tagSelectorTitle = getById('tag-selector-title');
        this.tagItems = getById('tag-selector-items');

        this.rowSelector = getById('row-selector');
        this.rowSelectorTitle = getById('row-selector-title');
        this.rowItems = getById('row-selector-items');

        this.inputModeTitle = getById('input-mode-title');
        this.inputModeItems = getById('input-mode-items');

        this.chooseAll = getById('choose-all');
        this.toggleAll = getById('toggle-all');

        this.review = getById('review');
        this.reviewTitle = getById('review-title');
        this.inputPhrase = getById('input-phrase');

        this.nextPage = getById('next-page');
        this.resetPage = getById('reset-page');
        this.submit = getById('submit');

        this.body = getByClass('body');

        this.wage = getById('wage');

        this.reviewMode = false;
        this.lastReview = 0;
        this.review.addEventListener('click', () => {
            this.reviewMode = !this.reviewMode;
            this.fetchReviewPhrases();
        });

        deactivate(this.rowSelector);
        deactivate(this.chooseAll);
        deactivate(this.toggleAll);
        deactivate(this.submit);
        deactivate(this.submit);
        deactivate(this.nextPage);
        deactivate(this.resetPage);

        this.chooseAll.addEventListener('click', this.chooseAllPhrases.bind(this));
        this.toggleAll.addEventListener('click', this.toggleAllPhrases.bind(this));
        this.submit.addEventListener('click', this.submitResult.bind(this));
        this.nextPage.addEventListener('click', this.fetchReviewPhrases.bind(this));
        this.resetPage.addEventListener('click', this.resetReviewPage.bind(this));
        this.inputPhrase.addEventListener('keydown', this.submitPhrase.bind(this));

        this.initContributorSelector();
        this.initTagSelector();
        this.initRowSelector();
        this.initInputModeSelector();
    }

    initInputModeSelector() {
        this.inputMode = 0;  // add
        deactivate(this.inputModeItems);
        this.inputModeTitle.addEventListener('click', () => {
            toggle(this.inputModeItems);
        });
    }

    initContributorSelector() {
        this.contributor = '';
        this.contributeWage = {tag: 0, add: 0};
    }

    initTagSelector() {
        const tagItemTemplate = template`<div class="selector__items__item" data-tag-id=${1} onclick="phrasePage.setTag(this)">${0}</div>`;

        // this.tagSelector = getById('tag-selector');
        this.tagItems.innerHTML = '';
        deactivate(this.tagItems);
        Request.get('/dev/api/language/phrase/tag')
            .then(data => {
                this.tagJar = {};
                data.forEach(tag => {
                    this.tagJar[tag.id] = tag.name;
                    const html = stringToHtml(tagItemTemplate(tag.name, tag.id));
                    this.tagItems.appendChild(html);
                });
        });

        this.tagSelectorTitle.addEventListener('click', () => {
            toggle(this.tagItems);
        });
    }

    initRowSelector() {
        const rowItemTemplate = template`<div class="selector__items__item" onclick="phrasePage.setRow(${1})">${0}</div>`;
        this.rows = 5;

        this.rowItems.innerHTML = '';
        deactivate(this.rowItems);

        [3, 4, 5, 6, 7, 8, 9].forEach(row => {
            const html = stringToHtml(rowItemTemplate(row, row));
            this.rowItems.appendChild(html);
        });

        this.rowSelectorTitle.addEventListener('click', () => {
            toggle(this.rowItems);
        });
    }

    addPhrases(phrases) {
        const phraseColumnTemplate = template`
            <div class="phrase-column">
                <div class="phrase-items"></div>
            </div>`;
        const phraseBoxTemplate = template`
            <div class="phrase-box ${2}" data-phrase-id=${1} onclick="phrasePage.choosePhrase(this)">
                <div class="phrase-box__char-box">${0}</div>
            </div>`;
        const subButton1 = `<div class="sub-btn" onclick="phrasePage.subChooseAllPhrases(this)">全选</div>`;
        const subButton2 = `<div class="sub-btn" onclick="phrasePage.subToggleAllPhrases(this)">反选</div>`;

        let phraseItems = [];
        phrases.forEach(phrase => {
            const html = stringToHtml(phraseBoxTemplate(phrase.cy, phrase.id, phrase.chosen ? 'active' : ''));
            phrase.element = html;
            phraseItems.push(html);
        });
        phraseItems.push(stringToHtml(subButton1));
        phraseItems.push(stringToHtml(subButton2));

        let phraseColumn = stringToHtml(phraseColumnTemplate());
        let phraseItemsElement = phraseColumn.getElementsByClassName('phrase-items')[0];
        phraseItems.forEach(phraseItem => phraseItemsElement.appendChild(phraseItem));
        // let html = stringToHtml(phraseColumnTemplate(phraseItems));
        this.body.appendChild(phraseColumn);
    }

    showPhraseMatrix() {
        this.body.innerHTML = '';
        const phraseMatrix = listToMatrix(this.phrases, this.rows);
        phraseMatrix.forEach(phrases => this.addPhrases(phrases));
    }

    setTag(tagElement) {
        this.tagId = Number.parseInt(tagElement.getAttribute('data-tag-id'));
        deactivate(this.tagItems);
        this.tagSelectorTitle.innerText = this.tagJar[this.tagId];
        if (this.reviewMode) {
            this.lastReview = 0;
            this.fetchReviewPhrases();
        } else {
            this.fetchPhrases();
        }
        noactivate(this.rowSelector);
        noactivate(this.chooseAll);
        noactivate(this.toggleAll);
        noactivate(this.submit);
    }

    fetchPhrases() {
        Request.get('/dev/api/language/phrase', {tag_id: this.tagId, count: 100})
            .then(data => {
                this.phrases = [];
                this.phraseJar = {};
                data.forEach(phrase => {
                    const phraseDict = {cy: phrase.cy, chosen: false, id: phrase.id};
                    this.phrases.push(phraseDict);
                    this.phraseJar[phrase.id] = phraseDict;
                });
                this.showPhraseMatrix();
            }).catch(ErrorHandler.handler);
    }

    resetReviewPage() {
        this.lastReview = 0;
        this.fetchReviewPhrases();
    }

    fetchReviewPhrases() {
        if (this.reviewMode) {
            noactivate(this.nextPage);
            noactivate(this.resetPage);
            activate(this.review);
            this.reviewTitle.innerText = '退出审核';
            if (this.tagId) {
                Request.get('/dev/api/language/phrase/review', {tag_id: this.tagId, count: 100, last: this.lastReview})
                    .then(body => {
                        this.phrases = [];
                        this.phraseJar = {};
                        body.object_list.forEach(tagMap => {
                            const phraseDict = {cy: tagMap.phrase.cy, chosen: tagMap.match, id: tagMap.phrase.id};
                            this.phrases.push(phraseDict);
                            this.phraseJar[tagMap.phrase.id] = phraseDict;
                        });
                        this.lastReview = body.next_value;
                        if (this.lastReview === null) {
                            deactivate(this.nextPage);
                        }
                        this.showPhraseMatrix();
                    }).catch(ErrorHandler.handler);
            }
        } else {
            deactivate(this.nextPage);
            deactivate(this.resetPage);
            noactivate(this.review);
            this.reviewTitle.innerText = '审核';
            this.lastReview = 0;
            if (this.tagId) {
                this.fetchPhrases();
            }
        }
    }

    setRow(row) {
        deactivate(this.rowItems);
        this.rowSelectorTitle.innerText = row;
        this.rows = row;
        this.showPhraseMatrix();
    }

    refreshWage() {
        this.wage.innerText = `标注工资：${this.contributeWage.tag.toFixed(1)}元，添词工资：${this.contributeWage.add.toFixed(2)}元`;
    }

    choosePhrase(phraseElement) {
        const phraseId = phraseElement.getAttribute('data-phrase-id');
        toggle(phraseElement);
        this.phraseJar[phraseId].chosen = !this.phraseJar[phraseId].chosen;
    }

    refreshPhrases() {
        this.phrases.forEach(phrase => {
            if (phrase.chosen) {
                activate(phrase.element);
            } else {
                deactivate(phrase.element);
            }
        });
    }

    chooseAllPhrases() {
        this.phrases.forEach(phrase => phrase.chosen = true);
        this.refreshPhrases();
    }

    toggleAllPhrases() {
        this.phrases.forEach(phrase => phrase.chosen = !phrase.chosen);
        this.refreshPhrases();
    }

    subChooseAllPhrases(element) {
        let phrases = element.parentNode.getElementsByClassName('phrase-box');
        phrases = Array.from(phrases);
        phrases.forEach(phraseElement => {
            const phraseId = phraseElement.getAttribute('data-phrase-id');
            activate(phraseElement);
            this.phraseJar[phraseId].chosen = true;
        });
    }

    subToggleAllPhrases(element) {
        let phrases = element.parentNode.getElementsByClassName('phrase-box');
        phrases = Array.from(phrases);
        phrases.forEach(this.choosePhrase.bind(this));
    }

    submitResult() {
        const matched = [];
        const unmatched = [];
        this.phrases.forEach(phrase => {
            if (phrase.chosen) {
                matched.push(phrase.id);
            } else {
                unmatched.push(phrase.id);
            }
        });

        let entrance = '';
        if (!this.reviewMode) {
            entrance = this.entranceId;
        }

        Request.put('/dev/api/language/phrase', {tag_id: this.tagId, matched: matched, unmatched: unmatched, entrance: entrance})
            .then(data => {
                if (this.reviewMode) {
                    this.fetchReviewPhrases();
                } else {
                    this.fetchPhrases();
                    this.contributeWage.tag += 0.1;
                    this.refreshWage();
                }
            }).catch(ErrorHandler.handler);
    }

    submitPhrase(event) {
        if (event.keyCode === 13) {
            if (!this.tagId) {
                alert('选择属性后才能搜索');
                return;
            }

            let cy = this.inputPhrase.value;
            this.inputPhrase.value = '';

            if (this.inputMode === 0) {
                Request.post('/dev/api/language/phrase', {
                    cy: cy,
                    entrance: this.entranceId,
                    action: 'add',
                }).then(data => {
                    const phraseDict = {cy: data.cy, chosen: false, id: data.id};
                    this.phrases.push(phraseDict);
                    this.phraseJar[data.id] = phraseDict;
                    this.showPhraseMatrix();
                    this.contributeWage.add += 0.02;
                    // this.contributeWage
                    this.refreshWage();
                }).catch(ErrorHandler.handler);
            } else {
                Request.post('/dev/api/language/phrase', {
                    cy: cy,
                    tag_id: this.tagId,
                    action: 'search',
                }).then(data => {
                    const phraseDict = {cy: data.phrase.cy, chosen: data.match, id: data.phrase.id};
                    this.phrases.push(phraseDict);
                    this.phraseJar[data.id] = phraseDict;
                    this.showPhraseMatrix();
                }).catch(ErrorHandler.handler);
            }
        }
    }

    setInputMode(inputMode) {
        this.inputMode = inputMode;
        this.inputModeTitle.innerText = ['添加', '搜索'][this.inputMode];
        deactivate(this.inputModeItems);
    }

    restoreEntrance() {
        Store.save('entrance', this.entranceId);
    }

    loadEntrance() {
        this.entrance.value = Store.load('entrance');
    }

    checkEntrance() {
        this.entranceId = this.entrance.value;
        Request.post('/dev/api/language/phrase/contributor', {entrance: this.entranceId})
            .then(data => {
                this.restoreEntrance();
                this.contributeWage = {tag: data.contribute_page / 10, add: data.add_count / 50};
                this.contributorSelectorTitle.innerText = data.contributor;
                this.refreshWage();
                deactivate(this.loginMask);
            }).catch(ErrorHandler.handler);
    }
}
