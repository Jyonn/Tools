class PhrasePage {
    constructor() {
        this.contributorSelector = getById('contributor-selector');
        this.contributorSelectorTitle = getById('contributor-selector-title');
        this.contributorItems = getById('contributor-selector-items');

        this.tagSelectorTitle = getById('tag-selector-title');
        this.tagItems = getById('tag-selector-items');

        this.rowSelector = getById('row-selector');
        this.rowSelectorTitle = getById('row-selector-title');
        this.rowItems = getById('row-selector-items');

        this.chooseAll = getById('choose-all');
        this.unchooseAll = getById('unchoose-all');
        this.toggleAll = getById('toggle-all');

        this.review = getById('review');
        this.reviewTitle = getById('review-title');

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
        deactivate(this.unchooseAll);
        deactivate(this.toggleAll);
        deactivate(this.submit);
        deactivate(this.submit);
        deactivate(this.nextPage);
        deactivate(this.resetPage);

        this.chooseAll.addEventListener('click', this.chooseAllPhrases.bind(this));
        this.unchooseAll.addEventListener('click', this.unchooseAllPhrases.bind(this));
        this.toggleAll.addEventListener('click', this.toggleAllPhrases.bind(this));
        this.submit.addEventListener('click', this.submitResult.bind(this));
        this.nextPage.addEventListener('click', this.fetchReviewPhrases.bind(this));
        this.resetPage.addEventListener('click', this.resetReviewPage.bind(this));

        this.initContributorSelector();
        this.initTagSelector();
        this.initRowSelector();
    }

    initContributorSelector() {
        this.contributor = '';
        this.contributeWage = 0;
        deactivate(this.contributorItems);
        this.contributorSelectorTitle.addEventListener('click', () => {
            toggle(this.contributorItems);
        })
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
        noactivate(this.unchooseAll);
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
            });
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
                    });
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

    setContributor(contributorElement) {
        deactivate(this.contributorItems);
        activate(this.contributorSelector);
        this.contributorSelectorTitle.innerText = contributorElement.innerText;
        this.contributor = contributorElement.innerText;

        Request.post('/dev/api/language/phrase/contributor', {contributor: this.contributor})
            .then(page => {
                this.contributeWage = page;
                this.refreshWage();
            })
    }

    refreshWage() {
        this.wage.innerText = `实时工资：${this.contributeWage / 10}元`;
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

    unchooseAllPhrases() {
        this.phrases.forEach(phrase => phrase.chosen = false);
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

        let contributor = '';
        if (!this.reviewMode) {
            contributor = this.contributor;
        }

        Request.put('/dev/api/language/phrase', {tag_id: this.tagId, matched: matched, unmatched: unmatched, contributor: contributor})
            .then(data => {
                if (this.reviewMode) {
                    this.fetchReviewPhrases();
                } else {
                    this.fetchPhrases();
                    this.contributeWage += 1;
                    this.refreshWage();
                }
            });
    }
}
