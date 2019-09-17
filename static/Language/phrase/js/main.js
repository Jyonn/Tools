class PhrasePage {
    constructor() {
        this.tagSelectorTitle = getById('tag-selector-title');
        this.tagItems = getById('tag-selector-items');

        this.rowSelector = getById('row-selector');
        this.rowSelectorTitle = getById('row-selector-title');
        this.rowItems = getById('row-selector-items');

        this.chooseAll = getById('choose-all');
        this.unchooseAll = getById('unchoose-all');
        this.toggleAll = getById('toggle-all');
        this.submit = getById('submit');

        this.body = getByClass('body');

        deactivate(this.rowSelector);
        deactivate(this.chooseAll);
        deactivate(this.unchooseAll);
        deactivate(this.toggleAll);
        deactivate(this.submit);

        this.chooseAll.addEventListener('click', this.chooseAllPhrases.bind(this));
        this.unchooseAll.addEventListener('click', this.unchooseAllPhrases.bind(this));
        this.toggleAll.addEventListener('click', this.toggleAllPhrases.bind(this));
        this.submit.addEventListener('click', this.submitResult.bind(this));

        this.initTagSelector();
        this.initRowSelector();
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

        let phraseItems = [];
        phrases.forEach(phrase => {
            const html = stringToHtml(phraseBoxTemplate(phrase.cy, phrase.id, phrase.chosen ? 'active' : ''));
            phrase.element = html;
            phraseItems.push(html);
        });

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
        this.fetchPhrases();
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

                activate(this.rowSelector);
                activate(this.chooseAll);
                activate(this.unchooseAll);
                activate(this.toggleAll);
                activate(this.submit);
            });
    }

    setRow(row) {
        deactivate(this.rowItems);
        this.rowSelectorTitle.innerText = row;
        this.rows = row;
        this.showPhraseMatrix();
    }

    choosePhrase(phraseElement) {
        const phraseId = phraseElement.getAttribute('data-phrase-id');
        toggle(phraseElement);
        this.phraseJar[phraseId].chosen = true;
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

        Request.put('/dev/api/language/phrase', {tag_id: this.tagId, matched: matched, unmatched: unmatched})
            .then(data => {
                this.fetchPhrases();
            });
    }
}
