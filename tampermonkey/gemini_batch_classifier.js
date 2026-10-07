// ==UserScript==
// @name         Gemini Batch Darija Classification - Thematic V1.0
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Automates Moroccan Darija thematic classification with Gemini.
// @author       You
// @match        https://gemini.google.com/*
// @grant        GM_openInTab
// ==/UserScript==

(function() {
    'use strict';

    const CONFIG = {
        targetUrl: "https://gemini.google.com/u/0/app",
        dbName: "Gemini_Darija_Classification_V1",
        storeName: "file_queue",
        networkSafetyDelay: 5000
    };

    const BASE_PROMPT = `Tu es un expert en classification de textes en Darija marocaine (arabe dialectal du Maroc).

## LABELS DISPONIBLES
- Politics_Society : politique, société, gouvernement, actualité, corruption, élections, relations internationales
- Business_Economy : économie, argent, business, investissement, bourse, impôts, salaires, entreprises, banques
- Sports : football, matchs, équipes marocaines (Raja, Wydad...), entraîneurs, joueurs, compétitions
- Health_Science : santé, médecine, maladies, traitements, médicaments, médecins, hôpitaux, symptômes
- Cuisine : recettes, plats marocains, cuisine, ingrédients, préparation des aliments, nourriture
- Religion : islam, prière, coran, hadith, ramadan, mosquée, pratiques religieuses, guidance spirituelle
- Nonsense : commentaires génériques, insultes, spam, textes trop courts, hors sujet, sans contenu thématique

## EXEMPLES ANNOTES PAR UN EXPERT HUMAIN

{"text": "1:52 نوض تريني نوض", "label": "Sports"}
{"text": "قلت ليهم على الحارس ديال الدزاير كون كان واعر كون حظروا القجع", "label": "Sports"}
{"text": "RA 7CHOUMA 3azouzi o lmrabt f montakhab o hrimaaat la", "label": "Sports"}
{"text": "المغرب ربحا 3 1 ورجعو ورا ماتش", "label": "Sports"}
{"text": "بصراحة والله خوتي المغاربة حنا لي غادي تجي فينا الدقة لاقدر الله وخرجنا من كأس إفريقيا", "label": "Sports"}
{"text": "نستمتع بيامال لاعب مستقبل كبير بس يبعد على ابوه و عبط شهرة", "label": "Sports"}
{"text": "Khona nta microbe 1 haja msg bguiti twaslo dyal nebdaw men 1957", "label": "Sports"}
{"text": "Machi wa9t dyal lkora dab aasi zabi", "label": "Nonsense"}
{"text": "أحسن الله إليك", "label": "Nonsense"}
{"text": "Bn courage t bkallah alikkk", "label": "Nonsense"}
{"text": "sat tbrklah sgir o kbir kifham tnx brooo", "label": "Nonsense"}
{"text": "والله اخويا إلا فيك السم ديال العيالات", "label": "Nonsense"}
{"text": "غير ترجل معانا بلا تمركين حنا معاك", "label": "Nonsense"}
{"text": "أحسنت أحسن الله إليك", "label": "Nonsense"}
{"text": "أغنياء الريع والفساد أثرياء الحروب والشتات يوجدون بكثرة في الصحراء المغربية", "label": "Politics_Society"}
{"text": "ايران اكبر عدو للمغرب وكل من يريد الشر لبلدي فهو عدوي الى يوم القيامة", "label": "Politics_Society"}
{"text": "عمل متعوب عليه لكن ذو قيمة عالية في تعريف الجيل الحالي تاريخهم", "label": "Politics_Society"}
{"text": "لا للفساد", "label": "Politics_Society"}
{"text": "مغاربة ايران جهلو", "label": "Politics_Society"}
{"text": "شكرا للتاريخ والشرح الساهل المفهوم عند الجميع", "label": "Politics_Society"}
{"text": "Pilota DWI 3LA HRIMAT", "label": "Politics_Society"}
{"text": "اصبح الطب في المغرب تجارة", "label": "Health_Science"}
{"text": "34 سنة الوزن ديالي 58 كيلو. ابحل المسمار.", "label": "Health_Science"}
{"text": "سلام دكتور فين عندك العيادة الله اخليك", "label": "Health_Science"}
{"text": "لم تتحدث على مرض مقاومة الانسولين و كسل الكبد و تشمع الكبد", "label": "Health_Science"}
{"text": "Bravo 3likom, ntoma chera7to lenass 7essan man wizara dyal de7a.", "label": "Health_Science"}
{"text": "مدخوب ولقينا المسران كله طايب بزاف داير لاكوليت ايكوغراف", "label": "Health_Science"}
{"text": "ولا دري صغير غيدخل خص يفتح قبل كاين واحد القانون ديال البلوك اوبيراتوار", "label": "Health_Science"}
{"text": "تبارك الله عليك. تحليل ممتاز", "label": "Business_Economy"}
{"text": "أخيييراً هاد النوع ديال المحتوى وصل للناس البورصة ماشي غير للخبراء", "label": "Business_Economy"}
{"text": "الضريبة على المقاول الذاتي واصلة ل 30%", "label": "Business_Economy"}
{"text": "3 المليار ديال دولار ماشي هي 30 مغربية هي 3000 مليار مغربية", "label": "Business_Economy"}
{"text": "السلام عليكم اخي انا خياط مسجل في منصومة cpu وكنخلص بربع السنوي", "label": "Business_Economy"}
{"text": "جيد جدا أخي على المجهود القيم لكن عندي لبس حيث قيمة الدرهم كتنزل", "label": "Business_Economy"}
{"text": "Salam Swinga information corriger f la video RAS dial TVA", "label": "Business_Economy"}
{"text": "Achman 3atriya dayal dajaj", "label": "Cuisine"}
{"text": "ننصحكم تجربوهم جااوني مزيانين بزاااف و يهبلوا", "label": "Cuisine"}
{"text": "ولش سميدة رقيقة ولا فينو", "label": "Cuisine"}
{"text": "كيفاش غادي نحافظ على السخونية نتاعهم إلا بغيت نبيعهم في البحر", "label": "Cuisine"}
{"text": "جربتووو جاا روووعة برااافو عليييك سمية متحرمناش من وصفاااتك", "label": "Cuisine"}
{"text": "بصحتك حبيبتي أني سيتو و جاني بنين ويهبل", "label": "Cuisine"}
{"text": "افضل قناة انا جربتو اخرجلي شحال بنين", "label": "Cuisine"}
{"text": "لا حول ولاقوة إلا بالله اللهم ارزقنا حسن الخاتمه", "label": "Religion"}
{"text": "سبحان آلله شحال عزيز علية هد الداعية سيد ياسين العمري", "label": "Religion"}
{"text": "ولا تاكلوا اموالكم بينكم بالباطل وتدلوا بها الى الحكام", "label": "Religion"}
{"text": "ولماذا تقول خطأ والمسألة فيها خلاف بل والراجح قول المالكية", "label": "Religion"}
{"text": "ma3riftk 3la salafia ghalt salafia makatchj3ch da3ich wla ay agenda", "label": "Religion"}
{"text": "لا إله إلا انت سبحانك اني كنت من الظالمين", "label": "Religion"}
{"text": "الحمد لله حتى يبلغ الحمد منتهاه", "label": "Religion"}

## RÈGLES IMPORTANTES
- Utilise UNIQUEMENT les 7 labels ci-dessus
- Si le texte mélange plusieurs sujets → choisis le sujet DOMINANT
- Mots religieux comme formule de politesse (الله يحفظك، تبارك الله) sans sujet religieux → Nonsense
- Texte trop court, générique ou incompréhensible → Nonsense
- Texte en français ou anglais pur sans contenu thématique → Nonsense

## TEXTES À CLASSIFIER
\`\`\`json
{transcript_content}
\`\`\`

## FORMAT DE RÉPONSE OBLIGATOIRE
Réponds UNIQUEMENT en JSON valide, sans explication, sans texte supplémentaire :
\`\`\`json
[
  {"id": "id_du_texte", "text": "texte", "label": "classe"}
]
\`\`\``;

    // --- DATABASE LOGIC ---
    const DB = {
        open: () => new Promise((resolve, reject) => {
            const r = indexedDB.open(CONFIG.dbName, 1);
            r.onupgradeneeded = e => e.target.result.createObjectStore(CONFIG.storeName, { keyPath: "id", autoIncrement: true });
            r.onsuccess = e => resolve(e.target.result);
            r.onerror = e => reject(e);
        }),
        addFiles: async (files) => {
            const db = await DB.open();
            const tx = db.transaction(CONFIG.storeName, "readwrite");
            const store = tx.objectStore(CONFIG.storeName);
            for (let f of files) store.add({ name: f.name, content: f, status: "pending", added: Date.now() });
            return new Promise(r => tx.oncomplete = r);
        },
        getNext: async () => {
            const db = await DB.open();
            return new Promise(resolve => {
                const tx = db.transaction(CONFIG.storeName, "readonly");
                const store = tx.objectStore(CONFIG.storeName);
                const req = store.openCursor();
                req.onsuccess = e => {
                    const c = e.target.result;
                    if (c && c.value.status === "pending") resolve(c.value);
                    else if (c) c.continue();
                    else resolve(null);
                };
            });
        },
        markDone: async (id) => {
            const db = await DB.open();
            const tx = db.transaction(CONFIG.storeName, "readwrite");
            const store = tx.objectStore(CONFIG.storeName);
            const r = store.get(id);
            r.onsuccess = () => { r.result.status = "done"; store.put(r.result); };
            return new Promise(r => tx.oncomplete = r);
        },
        count: async () => {
            const db = await DB.open();
            return new Promise(r => {
                const tx = db.transaction(CONFIG.storeName, "readonly");
                const req = tx.objectStore(CONFIG.storeName).getAll();
                req.onsuccess = () => r(req.result.filter(i => i.status === "pending").length);
            });
        },
        clearAll: async () => {
            const db = await DB.open();
            const tx = db.transaction(CONFIG.storeName, "readwrite");
            tx.objectStore(CONFIG.storeName).clear();
            return new Promise(r => tx.oncomplete = r);
        }
    };

    async function runLoop() {
        if (localStorage.getItem("LoopActive") !== "true") return;
        const fileData = await DB.getNext();
        if (!fileData) {
            localStorage.setItem("LoopActive", "false");
            alert("Batch Complete - Tous les fichiers ont ete traites !");
            return;
        }
        updateOverlay(`Processing: ${fileData.name}`);
        await delay(2500);
        let textContent = "";
        try {
            textContent = await fileData.content.text();
        } catch (e) {
            updateOverlay(`Erreur lecture : ${fileData.name}`);
            await delay(2000);
            await DB.markDone(fileData.id);
            GM_openInTab(CONFIG.targetUrl, { active: true, insert: true });
            return;
        }
        await delay(1000);
        const editor = document.querySelector('.ql-editor.textarea') || document.querySelector('.ql-editor');
        if (editor) {
            editor.focus();
            const finalPrompt = BASE_PROMPT.replace('{transcript_content}', textContent);
            document.execCommand('insertText', false, finalPrompt);
            editor.dispatchEvent(new Event('input', { bubbles: true }));
        }
        let sent = false;
        for (let i = 0; i < 100; i++) {
            const btn = document.querySelector('.send-button');
            const container = document.querySelector('.send-button-container');
            if (btn && container && !container.classList.contains('disabled')) {
                btn.click();
                sent = true;
                break;
            }
            await delay(500);
        }
        if (sent) {
            await delay(CONFIG.networkSafetyDelay);
            await DB.markDone(fileData.id);
            GM_openInTab(CONFIG.targetUrl, { active: true, insert: true });
        } else {
            window.location.reload();
        }
    }

    function delay(ms) { return new Promise(r => setTimeout(r, ms)); }
    function updateOverlay(msg) {
        const el = document.getElementById('status-msg');
        if(el) el.innerText = msg;
    }

    function createUI() {
        if (document.getElementById('batch-panel')) return;
        if (!document.body) { setTimeout(createUI, 500); return; }
        const panel = document.createElement('div');
        panel.id = "batch-panel";
        Object.assign(panel.style, {
            position: 'fixed', top: '80px', right: '20px', zIndex: '2147483647',
            background: '#1e1e1e', color: '#fff', padding: '15px', borderRadius: '12px',
            width: '240px', border: '2px solid #8ab4f8', fontSize: '13px',
            boxShadow: '0 4px 15px rgba(0,0,0,0.5)', fontFamily: 'sans-serif'
        });
        const header = document.createElement('div');
        header.style.cssText = "display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;";
        const title = document.createElement('h3');
        title.innerText = "Darija Classifier V1.0";
        title.style.cssText = "margin:0; color:#8ab4f8; font-size:14px;";
        const closeBtn = document.createElement('span');
        closeBtn.innerText = "X";
        closeBtn.style.cursor = "pointer";
        closeBtn.onclick = () => panel.style.display = 'none';
        header.appendChild(title);
        header.appendChild(closeBtn);
        panel.appendChild(header);
        const status = document.createElement('div');
        status.id = "status-msg";
        status.innerText = "Checking DB...";
        status.style.cssText = "margin-bottom:10px; background:#333; padding:5px; border-radius:4px; text-align:center;";
        panel.appendChild(status);
        const fileInput = document.createElement('input');
        fileInput.type = "file";
        fileInput.id = "files";
        fileInput.multiple = true;
        fileInput.accept = ".json";
        fileInput.style.cssText = "width:100%; margin-bottom:10px; font-size:11px;";
        panel.appendChild(fileInput);
        const btnLoad = document.createElement('button');
        btnLoad.innerText = "1. Charger les fichiers JSON";
        btnLoad.style.cssText = "width:100%; padding:8px; margin-bottom:8px; cursor:pointer; border-radius:4px; border:none; background:#444; color:white;";
        btnLoad.onclick = async () => {
            const f = fileInput.files;
            if(f.length) {
                await DB.addFiles(Array.from(f));
                const count = await DB.count();
                updateOverlay(`OK - ${f.length} fichiers. Total: ${count}`);
            }
        };
        panel.appendChild(btnLoad);
        const btnStart = document.createElement('button');
        btnStart.innerText = "2. LANCER ANNOTATION";
        btnStart.style.cssText = "width:100%; padding:12px; background:#8ab4f8; color:black; font-weight:bold; cursor:pointer; border-radius:4px; border:none;";
        btnStart.onclick = () => {
            localStorage.setItem("LoopActive", "true");
            runLoop();
        };
        panel.appendChild(btnStart);
        const btnStop = document.createElement('button');
        btnStop.innerText = "STOP / RESET";
        btnStop.style.cssText = "width:100%; padding:8px; margin-top:8px; background:#ff4641; color:white; cursor:pointer; border-radius:4px; border:none; font-size:11px;";
        btnStop.onclick = () => {
            localStorage.setItem("LoopActive", "false");
            window.location.reload();
        };
        panel.appendChild(btnStop);
        const btnClear = document.createElement('button');
        btnClear.innerText = "Vider la base de donnees";
        btnClear.style.cssText = "width:100%; padding:8px; margin-top:8px; background:#fbbc04; color:black; font-weight:bold; cursor:pointer; border-radius:4px; border:none; font-size:11px;";
        btnClear.onclick = async () => {
            if (confirm("Vider tous les fichiers en attente ?")) {
                await DB.clearAll();
                fileInput.value = "";
                updateOverlay("Base de donnees videe.");
            }
        };
        panel.appendChild(btnClear);
        document.body.appendChild(panel);
        DB.count().then(c => updateOverlay(`${c} fichiers en attente.`));
    }

    function init() {
        if (document.body) createUI();
        else setTimeout(init, 500);
    }
    init();
    if(localStorage.getItem("LoopActive") === "true") {
        setTimeout(runLoop, 4000);
    }
})();