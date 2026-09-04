const pptx=require("pptxgenjs"); const p=new pptx();
p.layout="LAYOUT_WIDE"; p.author="Shre Hari Prem Anandh"; p.title="Visualising Emotion";

// academic palette — restrained, university-formal
const NAVY="12232E", NAVY_D="0B1720", INK="1A2229", MUTED="4A545E", SUBTLE="6B747C";
const PAPER="FFFFFF", TINT="F4F6F7", RULE="D8DDE1", LINE="AEB6BC";
const TEAL="0D5C63", GOLD="9A6410", RED="9E3B33", GREEN="1E6B4F";
const HF="Cambria", BF="Calibri";
const W=13.33,H=7.5,M=0.75,CW=W-2*M;
const cols=(n,w)=>{const g=(CW-n*w)/(n-1);return [...Array(n)].map((_,i)=>M+i*(w+g));};
const CW2=(CW-0.32)/2, X2=M+CW2+0.32;   // two-column row: both cards end on the margin

function slide(dark){const s=p.addSlide();s.background={color:dark?NAVY:PAPER};return s;}
function head(s,kick,title,dark){
  s.addText(kick.toUpperCase(),{x:M,y:0.44,w:CW,h:0.26,isTextBox:true,margin:0,fontFace:BF,
    fontSize:11,bold:true,charSpacing:2,color:dark?"7FA8B5":TEAL});
  s.addText(title,{x:M,y:0.84,w:CW,h:0.98,isTextBox:true,margin:0,fontFace:HF,fontSize:32,
    bold:true,color:dark?PAPER:INK,valign:"middle"});
}
function foot(s,t,dark){s.addText(t,{x:M,y:H-0.86,w:CW,h:0.38,isTextBox:true,margin:0,fontFace:BF,
  fontSize:10.5,italic:true,color:dark?"93A6AE":SUBTLE,valign:"top"});}
function card(s,x,y,w,h,fill,edge){s.addShape(p.ShapeType.roundRect,
  {x,y,w,h,rectRadius:0.04,fill:{color:fill||TINT},line:{color:edge||RULE,width:1}});}
function body(s,t,x,y,w,h,sz,col){s.addText(t,{x,y,w,h,isTextBox:true,margin:0,fontFace:BF,
  fontSize:sz||13,color:col||MUTED,valign:"top"});}

/* ============================== 1 TITLE ============================== */
let s=slide(true);
s.addText("Visualising Emotion",{x:M,y:2.15,w:11.8,h:1.15,isTextBox:true,margin:0,
  fontFace:HF,fontSize:54,bold:true,color:PAPER});
s.addText("Measuring agreement between a written feeling and an AI-generated drawing",
  {x:M,y:3.35,w:11,h:0.6,isTextBox:true,margin:0,fontFace:HF,fontSize:21,italic:true,color:"B9C9D1"});
s.addShape(p.ShapeType.line,{x:M,y:4.25,w:3.0,h:0,line:{color:"3A5A6B",width:1.5}});
s.addText([{text:"Shre Hari Prem Anandh",options:{bold:true,breakLine:true}},
  {text:"MSc Artificial Intelligence · School of Computer Science",options:{breakLine:true}},
  {text:"University of Sheffield · Supervisor: Dr Chaona Chen",options:{}}],
  {x:M,y:4.55,w:8,h:1.2,isTextBox:true,margin:0,fontFace:BF,fontSize:14,color:"B9C9D1",lineSpacing:22});
s.addText("4 September 2026",{x:8.6,y:6.4,w:4,h:0.35,isTextBox:true,margin:0,fontFace:BF,
  fontSize:11,color:"7FA8B5",align:"right"});
s.addNotes("[20s] Good afternoon. My project measures whether an AI-generated drawing agrees emotionally with the words that produced it. The data is real: about a thousand members of the public at a science festival typed how they were feeling, and DALL-E drew each one.");

/* ============================== 2 THE QUESTION ======================= */
s=slide(); head(s,"The problem","Object prompts can be checked. Feelings cannot.");
card(s,M,2.05,CW2,1.72);
s.addText("“a red car”",{x:M+0.35,y:2.25,w:5,h:0.5,isTextBox:true,margin:0,fontFace:HF,fontSize:22,bold:true,color:INK});
body(s,"Is there a car? Is it red? The prompt names objects, so existing metrics can score it.",M+0.35,2.82,CW2-0.7,0.85,13.5);
card(s,X2,2.05,CW2,1.72,"FBF6EC",GOLD);
s.addText("“tired but happy”",{x:X2+0.35,y:2.25,w:5,h:0.5,isTextBox:true,margin:0,fontFace:HF,fontSize:22,bold:true,color:INK});
body(s,"No object to find, no answer key, and the feeling is mixed. Existing metrics do not transfer.",X2+0.35,2.82,CW2-0.7,0.85,13.5);
card(s,M,4.15,CW,1.42,"EEF2F3",TEAL);
s.addText("Research question",{x:M+0.35,y:4.32,w:11,h:0.3,isTextBox:true,margin:0,fontFace:BF,fontSize:12,bold:true,color:TEAL});
s.addText("To what extent does an automatic image-emotion reader agree with prompt-derived emotion labels for AI-generated monochrome drawings, and how does that agreement vary by visual content and by repeated prompts?",
  {x:M+0.35,y:4.68,w:11.1,h:0.82,isTextBox:true,margin:0,fontFace:HF,fontSize:15.5,color:INK,valign:"top"});
body(s,"Sub-questions:  (i) does agreement exceed a random-pairing baseline?   (ii) does it differ for face-classified and scene-classified drawings?   (iii) how stable is the image reading when the same prompt is drawn again?   (iv) does describe-then-extract agree more than reading emotion from the image directly?",
  M,5.92,CW,0.85,12.5);
foot(s,"The question is deliberately narrower than “does the drawing convey the feeling” — see the closing slide.");
s.addNotes("[50s] You can check 'a red car' — look for a car, check it's red. That is what text-to-image evaluation does today. But 'tired but happy' has no object and no correct answer. So my research question is deliberately precise: to what extent does an automatic image-emotion reader AGREE with the emotion read from the prompt. Four sub-questions follow from it, and each one becomes a result.");

/* ============================== 3 THE GAP =========================== */
s=slide(); head(s,"Literature","Four established areas, and the space between them");
const G=[["Emotion in text","Well established. GoEmotions supplies a 27-category taxonomy and a classifier; but short first-person self-report is the hardest register.",GREEN],
["Emotional image generation","Well established. Systems generate images to carry a chosen emotion, and colour is reported as the principal carrier of affect.",GREEN],
["Text-to-image evaluation","Well established for OBJECTS. CLIPScore and VQAScore measure whether the picture contains what the prompt named.",GREEN],
["Reading emotion from an image","Weak. Vision-language models are positively biased and order-sensitive readers of affect.",GOLD]];
G.forEach((g,i)=>{const y=1.98+i*0.86;
  s.addShape(p.ShapeType.ellipse,{x:M,y:y+0.1,w:0.26,h:0.26,fill:{color:g[2]},line:{type:"none"}});
  s.addText(g[0],{x:M+0.45,y:y,w:3.6,h:0.66,isTextBox:true,margin:0,fontFace:BF,fontSize:14,bold:true,color:INK,valign:"top"});
  body(s,g[1],4.45,y,8.15,0.66,13);});
card(s,M,5.42,CW,1.05,"EEF2F3",TEAL);
s.addText("The gap: no study has measured whether the emotion in a person's own unedited self-report is recoverable from the drawing generated from it — in monochrome line art, where the reported colour channel is absent.",
  {x:M+0.35,y:5.55,w:11.1,h:0.8,isTextBox:true,margin:0,fontFace:HF,fontSize:16,bold:true,color:TEAL,valign:"middle"});
foot(s,"97 papers screened; 73 retained as core evidence across eight themes. Colour is cited as motivation only — this study has no colour-control condition.");
s.addNotes("[50s] Four areas are each well established on their own. Reading emotion from text. Generating emotional images — where the literature says colour carries most of the affect. Evaluating text-to-image output, but for objects, not feelings. And reading emotion back out of an image, which is known to be weak and positively biased. The gap sits between them. I should be explicit: I cite the colour work as motivation for why line art is hard. I have no colour condition, so I make no claim about colour.");

/* ============================== 4 CONTRIBUTION ====================== */
s=slide(true); head(s,"Contribution","Similarity, not matching",true);
s.addText("“Asking whether the image emotion matches the text — right or wrong — is too simplistic. Emotion is subjective, there is no ground truth, humans disagree and models are noisy. Ask how similar the two emotions are.”",
  {x:M,y:1.95,w:11.5,h:1.35,isTextBox:true,margin:0,fontFace:HF,fontSize:19,italic:true,color:"D6E3E9",valign:"top"});
s.addText("— Supervisory direction, 30 July 2026",{x:M,y:3.32,w:6,h:0.3,isTextBox:true,margin:0,
  fontFace:BF,fontSize:11.5,color:"7FA8B5"});
const CB=[["Conventional","One-to-one match. The predicted label is right or wrong; accuracy is reported against an assumed ground truth."],
["This project","A four-level similarity ladder over emotion families. “Happy” and “excited” are counted as close, not as a miss — and every level is referenced to chance."]];
CB.forEach((c,i)=>{const x=M+i*6.05;
  card(s,x,3.85,5.75,1.6,i?"14333B":"16232C",i?"2F7B7F":"33424D");
  s.addText(c[0],{x:x+0.35,y:4.02,w:5,h:0.35,isTextBox:true,margin:0,fontFace:BF,fontSize:13,bold:true,color:i?"7FC4BE":"9FB0B9"});
  s.addText(c[1],{x:x+0.35,y:4.4,w:5.05,h:1.0,isTextBox:true,margin:0,fontFace:BF,fontSize:13,color:i?"D6E3E9":"9FB0B9",valign:"top"});});
s.addText("This is the novel element: the field reports one-to-one accuracy; this study reports graded, chance-referenced similarity.",
  {x:M,y:5.75,w:11.6,h:0.55,isTextBox:true,margin:0,fontFace:HF,fontSize:17,bold:true,color:PAPER,valign:"middle"});
s.addNotes("[60s] This is the contribution, and my supervisor named it. Emotion is subjective. There is no ground truth. Humans disagree with each other and the models are noisy. So asking whether the image emotion MATCHES the text, right or wrong, is too simplistic. Instead I measure how SIMILAR the two readings are, on a four-level ladder over emotion families, so that 'happy' and 'excited' count as close rather than as a miss. That is the novel element — the field reports one-to-one accuracy; I report graded similarity, and every level is referenced to chance.");

/* ============================== 5 METHOD ============================ */
s=slide(); head(s,"Methodology","Describe the image, then read the feeling from the description");
// diagram
const bx=(x,y,w,h,t,sub,fill,edge,tc)=>{card(s,x,y,w,h,fill,edge);
  s.addText(t,{x:x+0.15,y:y+0.16,w:w-0.3,h:0.34,isTextBox:true,margin:0,fontFace:BF,fontSize:13,bold:true,color:tc||INK,align:"center"});
  s.addText(sub,{x:x+0.15,y:y+0.53,w:w-0.3,h:0.6,isTextBox:true,margin:0,fontFace:BF,fontSize:11,color:tc?"D6E3E9":SUBTLE,align:"center",valign:"top"});};
const arrow=(x,y,w)=>s.addShape(p.ShapeType.line,{x,y,w,h:0,
  line:{color:LINE,width:1.75,endArrowType:"triangle"}});
const D1=M, D2=3.76, D3=6.87, D4=9.98, DW=2.6;
bx(D1,2.1,2.5,1.3,"Drawing","1,025 monochrome\nline drawings",TINT);
arrow(D1+2.56,2.75,0.39);
bx(D2,2.1,DW,1.3,"BLIP-VQA","five factual questions\n-> one neutral sentence",TINT);
arrow(D2+DW+0.06,2.75,0.39);
bx(D3,2.1,DW,1.3,"BART-MNLI","zero-shot over\nseven emotion families",TINT);
arrow(D3+DW+0.06,2.75,0.39);
bx(D4,2.1,DW,1.3,"Image reading","top-3 emotions",TINT,TEAL);
bx(D1,3.75,2.5,1.3,"Prompt","the visitor's own\nwords",TINT);
arrow(D1+2.56,4.4,0.39);
bx(D2,3.75,DW,1.3,"GoEmotions","28 labels collapsed to\nthe same seven families",TINT);
arrow(D2+DW+0.06,4.4,D4-(D2+DW)-0.12);
bx(D4,3.75,DW,1.3,"Prompt reading","top-3 emotions",TINT,TEAL);
card(s,M,5.35,CW,1.12,"EEF2F3",TEAL);
s.addText("Compare  →  four-level similarity ladder, every level against a 300-shuffle random-pairing null",
  {x:M+0.35,y:5.5,w:11.2,h:0.35,isTextBox:true,margin:0,fontFace:BF,fontSize:13.5,bold:true,color:TEAL});
["valence-arousal distance","valence-sign agreement","emotion-family agreement","top-3 overlap"]
  .forEach((m,i)=>body(s,"- "+m,M+0.35+i*2.86,5.88,2.8,0.4,12.5,MUTED));
foot(s,"The image model is asked only factual questions. Caveat stated in the write-up: “what is the facial expression?” often returns a feeling word, so the separation is weaker than it appears.");
s.addNotes("[60s] My supervisor's instruction was: don't force CLIP to output an emotion, because CLIP is trained on real colour photographs and is good at objects, not affect. So the image is DESCRIBED first — five factual questions to BLIP-VQA, assembled into one neutral sentence — and a separate language model reads the feeling out of that sentence. The prompt goes through GoEmotions into the same seven families. Now both sides are text, and I compare text to text on a four-level ladder. I should flag one honest caveat: asking 'what is the facial expression' often returns a feeling word, so the separation is weaker than it first appears.");

/* ============================== 6 DATA ============================== */
s=slide(); head(s,"Data","1,025 real self-reports, and what it took to use them");
const st=(x,big,lab,col)=>{s.addText(big,{x,y:1.95,w:2.85,h:0.72,isTextBox:true,margin:0,fontFace:HF,
  fontSize:36,bold:true,color:col,valign:"bottom"});
  body(s,lab,x,2.75,2.85,0.85,12.5);};
const c6=cols(4,2.85);
st(c6[0],"1,012","analysed records\n(13 pre-festival tests excluded)",NAVY);
st(c6[1],"607 / 405","prompts carrying a feeling\nversus not — the specificity set",TEAL);
st(c6[2],"591 / 421","face-classified versus\nscene-classified drawings",TEAL);
st(c6[3],"87","prompts drawn more than once,\ncovering 336 records",GOLD);
card(s,M,3.85,CW2,2.7);
s.addText("Data engineering",{x:M+0.32,y:4.02,w:CW2-0.64,h:0.32,isTextBox:true,margin:0,fontFace:BF,fontSize:13,bold:true,color:INK});
s.addText([{text:"Three incompatible filename schemes in one folder — a naive loader resolves under 20%.",options:{bullet:true,breakLine:true}},
{text:"C2PA signing timestamps recovered from inside each PNG identified 13 pre-festival developer tests.",options:{bullet:true,breakLine:true}},
{text:"Ran to completion on all 1,025 images with no unhandled errors — a robustness statement, not an accuracy one.",options:{bullet:true}}],
{x:M+0.32,y:4.42,w:CW2-0.64,h:1.95,isTextBox:true,margin:0,fontFace:BF,fontSize:12.5,color:MUTED,paraSpaceAfter:5});
card(s,X2,3.85,CW2,2.7);
s.addText("Data pre-processing",{x:X2+0.32,y:4.02,w:CW2-0.64,h:0.32,isTextBox:true,margin:0,fontFace:BF,fontSize:13,bold:true,color:INK});
s.addText([{text:"Eight records contained names of private individuals; these were replaced with a placeholder.",options:{bullet:true,breakLine:true}},
{text:"Detection combined a 7,944-name gazetteer, a 236,000-word dictionary and naming phrases — 77% of the corpus is lower case, so capitalisation alone would miss most names.",options:{bullet:true,breakLine:true}},
{text:"Verified inert: re-running the prompt reader changed no emotion label.",options:{bullet:true}}],
{x:X2+0.32,y:4.42,w:CW2-0.64,h:1.95,isTextBox:true,margin:0,fontFace:BF,fontSize:12.5,color:MUTED,paraSpaceAfter:5});
s.addNotes("[45s] A thousand and twenty-five real self-reports. Three things had to be solved before any analysis. Three different filename systems — a naive loader finds under a fifth of the files. Hidden C2PA signing timestamps inside each PNG, which let me identify thirteen images made before the festival: developer tests, excluded. And a pre-processing step: eight records contained real names, replaced with a placeholder, and I verified that redaction changed no emotion label at all.");

/* ============================== 7 RIGOUR ============================ */
s=slide(true); head(s,"Evaluation design","Two checks that decide whether any number means anything",true);
card(s,M,2.05,CW2,1.78,"16232C","33424D");
s.addText("1 · A random-pairing null",{x:M+0.35,y:2.2,w:CW2-0.7,h:0.34,isTextBox:true,margin:0,fontFace:BF,fontSize:13.5,bold:true,color:"7FC4BE"});
s.addText("Within each subset the image side is shuffled and re-paired against the untouched prompts, 300 times, with a fixed seed. Every figure I report is quoted against its own null, so a result counts only insofar as it exceeds chance.",
  {x:M+0.35,y:2.62,w:CW2-0.7,h:1.35,isTextBox:true,margin:0,fontFace:BF,fontSize:13,color:"C6D4DB",valign:"top"});
card(s,X2,2.05,CW2,1.78,"16232C","33424D");
s.addText("2 · A specificity check",{x:X2+0.35,y:2.2,w:CW2-0.7,h:0.34,isTextBox:true,margin:0,fontFace:BF,fontSize:13.5,bold:true,color:"7FC4BE"});
s.addText("405 prompts carry no feeling — “pigs”, “mickey mouse”. On these the valence–arousal metric returns 76.6% against a null of 76.6%, z = +0.3. The pipeline reports agreement only where the prompt reader finds an emotion.",
  {x:X2+0.35,y:2.62,w:CW2-0.7,h:1.35,isTextBox:true,margin:0,fontFace:BF,fontSize:13,color:"C6D4DB",valign:"top"});
// the floor/chance ruler
s.addText("And the scale does not start at zero",{x:M,y:4.45,w:8,h:0.36,isTextBox:true,margin:0,
  fontFace:BF,fontSize:13.5,bold:true,color:PAPER});
const RX=M,RY=5.0,RW=CW, at=v=>RX+((v-41)/59)*RW;
card(s,RX,RY,RW,0.5,"16232C","33424D");
s.addShape(p.ShapeType.rect,{x:RX,y:RY,w:at(76)-RX,h:0.5,fill:{color:"1E3A42"},line:{type:"none"}});
[[41,"9FB0B9"],[76,PAPER],[84,"D9A441"]].forEach(t=>
  s.addShape(p.ShapeType.rect,{x:t[0]===41?RX:at(t[0]),y:RY-0.14,w:0.035,h:0.78,fill:{color:t[1]},line:{type:"none"}}));
[[41,"41 - metric floor","9FB0B9","left"],[76,"76 - random pairings",PAPER,"center"],[84,"84 - observed","D9A441","center"]]
 .forEach(t=>s.addText(t[1],{x:t[0]===41?RX:at(t[0])-1.5,y:RY+0.62,w:3,h:0.32,isTextBox:true,
   margin:0,fontFace:BF,fontSize:12,bold:true,color:t[2],align:t[3]}));
foot(s,"Consequence: a valence–arousal score of 71 reads as a pass but is below chance. Reporting therefore leads with valence-sign and family agreement, which the metric cannot substitute for.",true);
s.addNotes("[70s] This is the slide I would most like you to take away. Two checks decide whether any of my numbers mean anything. First, every figure is measured against a random-pairing null — I shuffle the images against the prompts three hundred times and see what chance alone produces. Second, a specificity check: four hundred prompts contain no feeling at all, things like 'pigs' and 'mickey mouse', and on those the pipeline sits exactly on chance. It reports agreement only where there is emotion to find. And third — the scale does not start at zero. The valence-arousal metric has a floor of forty-one and random pairs already score seventy-six. So a seventy-one looks like a pass and is actually below chance. That is why I lead with the other two measures.");

/* ============================== 8 RESULTS =========================== */
s=slide(); head(s,"Results","Agreement is above chance, and strongest for face-classified drawings");
s.addTable([
 [{text:"Subset",options:{bold:true}},{text:"Valence-sign agreement",options:{bold:true}},
  {text:"Emotion-family agreement",options:{bold:true}},{text:"Verdict",options:{bold:true}}],
 ["Emotional prompts  (n=607)","64.0%   vs null 45.6%   z +11.1","53.1%   vs null 38.8%   z +10.3","Well above chance"],
 ["Face-classified  (n=402)","73.9%   vs null 53.5%   z +10.4","61.9%   vs null 45.8%   z +10.3","Strongest"],
 ["Scene-classified  (n=205)","42.9%   vs null 29.6%   z +5.8","35.6%   vs null 26.2%   z +4.4","Above chance, weaker"],
 ["Non-emotional  (n=405)","— degenerate by definition","— degenerate by definition","Specificity check"],
],{x:M,y:2.06,w:CW,colW:[3.0,3.3,3.3,2.23],fontFace:BF,fontSize:12,color:INK,
   border:{type:"solid",color:RULE,pt:1},fill:{color:PAPER},align:"left",valign:"middle",rowH:0.42});
const R=[["Repeated prompts","Given the same prompt text, the image reader returns the same emotion for 68.8% of drawings within a group, against a permutation null of 59.1% (z +4.9). The generator is not deterministic in what the reader recovers."],
["Method comparison","Holding the prompt reader constant and varying only the image reader: describe-then-extract 49.3% family agreement against direct-CLIP 25.3%. Note the prompt reader here is BART-MNLI, not the GoEmotions reader used above."],
["Robustness","Re-run on the 763 distinct prompts, the overall and face results hold (z +9 to +11). The scene result weakens substantially, to 37.3% (z +3.5)."]];
R.forEach((r,i)=>{const y=4.58+i*0.8;
  s.addText(r[0],{x:M,y:y,w:2.55,h:0.72,isTextBox:true,margin:0,fontFace:BF,fontSize:12.5,bold:true,color:TEAL,valign:"top"});
  body(s,r[1],M+2.75,y,9.08,0.78,12.5);});
foot(s,"No formal significance test of the face–scene difference has been run; both rates are reported against their own nulls instead.");
s.addNotes("[70s] Agreement is well above chance overall — sixty-four per cent valence-sign against a null of forty-six, z over eleven. It is strongest for face-classified drawings at seventy-four per cent, and weaker but still above chance for scenes. On the non-emotional prompts the sign and family measures are degenerate by the subset's own definition, so I report only the valence-arousal specificity result there. Three further results. Repeated prompts: the reader recovers the same emotion sixty-nine per cent of the time against a fifty-nine per cent null. The method comparison favours describe-then-extract, roughly double, though I should note the prompt reader differs between the two arms. And on distinct prompts only, the face result holds while the scene result weakens substantially — I report that rather than claiming everything survives.");

/* ============================== 9 DEMO ============================== */
s=slide(true); head(s,"Demonstration","The pipeline, running live",true);
card(s,M,2.15,CW,2.22,"16232C","33424D");
const D=[["Choose a drawing","from the festival dataset, or upload an image"],
["Watch it described","the five factual answers, then the emotion read from them"],
["Compare","both readings, and the score against the chance line"]];
const c9=cols(3,3.9);
D.forEach((d,i)=>{
  s.addShape(p.ShapeType.ellipse,{x:c9[i]+0.28,y:2.5,w:0.5,h:0.5,fill:{color:"1E3A42"},line:{color:"2F7B7F",width:1}});
  s.addText(String(i+1),{x:c9[i]+0.28,y:2.5,w:0.5,h:0.5,isTextBox:true,margin:0,fontFace:BF,
    fontSize:13,bold:true,color:"7FC4BE",align:"center",valign:"middle"});
  s.addText(d[0],{x:c9[i]+0.28,y:3.15,w:3.35,h:0.35,isTextBox:true,margin:0,fontFace:BF,fontSize:14,bold:true,color:PAPER});
  s.addText(d[1],{x:c9[i]+0.28,y:3.55,w:3.35,h:1.0,isTextBox:true,margin:0,fontFace:BF,fontSize:12.5,color:"C6D4DB",valign:"top"});});
s.addText("Every figure the interface shows is referenced to the measured chance line, and nothing a visitor types is stored.",
  {x:M,y:4.72,w:11.6,h:0.5,isTextBox:true,margin:0,fontFace:BF,fontSize:13.5,color:"C6D4DB"});
s.addNotes("[90 SECONDS — LIVE DEMO] Switch to the browser. Pick the sad example. Talk through: here are the five factual answers the image model gave. Here is the feeling the language model read out of that description. Here is what GoEmotions read from the words. And here is the comparison — note the chance line, and that the headline says 'closer than N per cent of random pairings' rather than a bare score. Keep it to ninety seconds and return to the slides.");

/* ============================== 10 CLOSE ============================ */
s=slide(); head(s,"Conclusion","What this establishes, and what it does not");
card(s,M,1.98,CW2,2.72,"EEF2F3",TEAL);
s.addText("Established",{x:M+0.32,y:2.15,w:CW2-0.64,h:0.32,isTextBox:true,margin:0,fontFace:BF,fontSize:13,bold:true,color:TEAL});
s.addText([{text:"Prompt-reader and image-reader agreement is well above chance on every metric.",options:{bullet:true,breakLine:true}},
{text:"Agreement is substantially higher for face-classified than scene-classified drawings.",options:{bullet:true,breakLine:true}},
{text:"The same prompt does not reliably yield the same recovered emotion (69% vs 59% null).",options:{bullet:true,breakLine:true}},
{text:"Describe-then-extract agrees more than reading emotion from the image directly.",options:{bullet:true}}],
{x:M+0.32,y:2.55,w:CW2-0.64,h:2.05,isTextBox:true,margin:0,fontFace:BF,fontSize:12.5,color:MUTED,paraSpaceAfter:4});
card(s,X2,1.98,CW2,2.72,"FBF6EC",GOLD);
s.addText("Not established",{x:X2+0.32,y:2.15,w:CW2-0.64,h:0.32,isTextBox:true,margin:0,fontFace:BF,fontSize:13,bold:true,color:GOLD});
s.addText([{text:"What a human viewer perceives — both readers are automatic, and they disagree with each other.",options:{bullet:true,breakLine:true}},
{text:"That the face–scene gap is statistically significant; no formal test has been run.",options:{bullet:true,breakLine:true}},
{text:"Any effect of colour — the corpus is monochrome but there is no colour condition.",options:{bullet:true,breakLine:true}},
{text:"Any positive-versus-negative direction; that claim was withdrawn.",options:{bullet:true}}],
{x:X2+0.32,y:2.55,w:CW2-0.64,h:2.05,isTextBox:true,margin:0,fontFace:BF,fontSize:12.5,color:MUTED,paraSpaceAfter:4});
card(s,M,4.95,CW,0.85);
s.addText("Future work:  human validation of both readers  ·  sketch-trained describers  ·  a formal test and confidence intervals for the face–scene difference",
  {x:M+0.32,y:5.08,w:11.2,h:0.6,isTextBox:true,margin:0,fontFace:BF,fontSize:13,color:MUTED,valign:"middle"});
s.addText("The contribution is a chance-referenced similarity measure for emotional agreement, not a new classifier.",
  {x:M,y:6.02,w:12.0,h:0.44,isTextBox:true,margin:0,fontFace:HF,fontSize:17.5,bold:true,color:INK});
s.addText("Thank you — questions welcome",{x:M,y:6.66,w:6,h:0.4,isTextBox:true,margin:0,fontFace:HF,
  fontSize:15,italic:true,color:SUBTLE});
s.addNotes("[60s] To close. Established: agreement well above chance on every metric; substantially higher for face-classified drawings; the same prompt does not reliably give the same recovered emotion; and describe-then-extract agrees more than asking the image model directly. Not established, and I want to say these before you ask: what a human perceives — both my readers are automatic and they disagree with each other; whether the face-scene gap is statistically significant, since no formal test has been run; anything about colour; and any positive-versus-negative direction, which I withdrew. The contribution is the chance-referenced similarity measure itself, not a new classifier. Thank you.");

p.writeFile({fileName:"Visualising_Emotion_Final.pptx"}).then(f=>console.log("written:",f));
