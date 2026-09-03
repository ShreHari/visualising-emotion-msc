const pptx = require("pptxgenjs");
const p = new pptx();
p.layout = "LAYOUT_WIDE";                     // 13.3 x 7.5
p.author = "Shre Hari Prem Anandh";
p.title  = "Visualising Emotion";

// ---- palette: the project's own instrument colours -------------------------
const TEAL="0D5C63", TEAL_D="072F33", PAPER="F7F5F1", WHITE="FFFFFF";
const INK="14161A", MUTED="4F545B", SUBTLE="6E747B", RULE="DDD8CF";
const GOLD="B87614", BLUE="2F6FD0", RED="C93A3A", GREEN="1E6B4F";
const HFONT="Cambria", BFONT="Calibri";

const W=13.33, H=7.5, M=0.7, CW=W-2*M;
// evenly pitched columns: n cards of width w across the content band
function cols(n,w){ const gap=(CW-n*w)/(n-1); return [...Array(n)].map((_,i)=>M+i*(w+gap)); }

// ---- motif: filled dot = the words, ring = the drawing ---------------------
function motif(s, x, y, r, colFill, colRing, gapW){
  s.addShape(p.ShapeType.line,{x:x,y:y+r,w:gapW,h:0,line:{color:colRing,width:2.5,dashType:"solid"}});
  s.addShape(p.ShapeType.ellipse,{x:x-r,y:y,w:r*2,h:r*2,fill:{color:colFill},line:{type:"none"}});
  s.addShape(p.ShapeType.ellipse,{x:x+gapW-r,y:y,w:r*2,h:r*2,fill:{color:"FFFFFF"},
    line:{color:colRing,width:2.5}});
}

function titleOf(s, txt, dark){
  s.addText(txt,{x:M,y:0.88,w:CW,h:0.82,isTextBox:true,margin:0,
    fontFace:HFONT,fontSize:34,bold:true,color:dark?WHITE:INK,align:"left",valign:"middle"});
}
function kicker(s, txt, dark){
  s.addText(txt.toUpperCase(),{x:M,y:0.50,w:CW,h:0.3,isTextBox:true,margin:0,
    fontFace:BFONT,fontSize:11,bold:true,charSpacing:2,color:dark?"7FC4BE":TEAL});
}
function note(s, txt, dark){
  s.addText(txt,{x:M,y:H-0.88,w:CW,h:0.4,isTextBox:true,margin:0,
    fontFace:BFONT,fontSize:11,italic:true,color:dark?"9FB4B3":SUBTLE});
}
function light(){ const s=p.addSlide(); s.background={color:PAPER}; return s; }
function dark(){  const s=p.addSlide(); s.background={color:TEAL_D}; return s; }

function statCard(s,x,y,w,big,small,col){
  s.addText(big,{x:x,y:y,w:w,h:0.9,isTextBox:true,margin:0,fontFace:HFONT,fontSize:48,
    bold:true,color:col,align:"left",valign:"bottom"});
  s.addText(small,{x:x,y:y+0.95,w:w,h:0.85,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:13,color:MUTED,align:"left",valign:"top"});
}

/* ==================================================== 1. TITLE ============ */
let s=dark();
motif(s, 1.0, 1.35, 0.13, "FFFFFF", "7FC4BE", 1.5);
s.addText("Visualising Emotion",{x:M,y:2.0,w:11.6,h:1.25,isTextBox:true,margin:0,
  fontFace:HFONT,fontSize:60,bold:true,color:WHITE});
s.addText("Does an AI drawing carry the feeling in the words that made it?",
  {x:M,y:3.3,w:10.6,h:0.75,isTextBox:true,margin:0,fontFace:HFONT,fontSize:24,
   italic:true,color:"BFD9D6"});
s.addShape(p.ShapeType.line,{x:M,y:4.35,w:3.2,h:0,line:{color:"2F7B7F",width:1.5}});
s.addText([
  {text:"Shre Hari Prem Anandh",options:{bold:true,breakLine:true}},
  {text:"MSc Artificial Intelligence · University of Sheffield",options:{breakLine:true}},
  {text:"Supervisor: Dr Chaona Chen",options:{}},
],{x:M,y:4.65,w:8,h:1.3,isTextBox:true,margin:0,fontFace:BFONT,fontSize:14,color:"BFD9D6",lineSpacing:22});
s.addText("1,025 real self-reports · 1,012 analysed · 28/28 tests passing",
  {x:7.9,y:6.55,w:4.75,h:0.4,isTextBox:true,margin:0,fontFace:BFONT,fontSize:11,
   color:"7FC4BE",align:"right"});
s.addNotes("Good afternoon. My project asks whether an AI drawing actually carries the feeling that was in the words used to make it. The data is real: about a thousand members of the public at a science festival typed how they felt, and DALL-E drew each one.");

/* ==================================================== 2. THE PROBLEM ====== */
s=light(); kicker(s,"The problem"); titleOf(s,"Some prompts can be checked. Feelings cannot.");
s.addShape(p.ShapeType.roundRect,{x:M,y:2.05,w:5.75,h:4.15,rectRadius:0.06,
  fill:{color:WHITE},line:{color:RULE,width:1}});
s.addText("“a red car”",{x:M+0.4,y:2.4,w:5,h:0.6,isTextBox:true,margin:0,
  fontFace:HFONT,fontSize:28,bold:true,color:INK});
s.addText([
  {text:"Is there a car?",options:{bullet:true,breakLine:true}},
  {text:"Is it red?",options:{bullet:true,breakLine:true}},
  {text:"Done — the prompt names objects.",options:{bullet:true}},
],{x:M+0.4,y:3.2,w:5,h:1.8,isTextBox:true,margin:0,fontFace:BFONT,fontSize:16,
   color:MUTED,paraSpaceAfter:8});
s.addText("This is what almost all text-to-image evaluation does.",
  {x:M+0.4,y:5.35,w:5,h:0.6,isTextBox:true,margin:0,fontFace:BFONT,fontSize:13,
   italic:true,color:GREEN});

s.addShape(p.ShapeType.roundRect,{x:6.9,y:2.05,w:5.75,h:4.15,rectRadius:0.06,
  fill:{color:"FBF3E7"},line:{color:GOLD,width:1}});
s.addText("“tired but happy”",{x:7.3,y:2.4,w:5,h:0.6,isTextBox:true,margin:0,
  fontFace:HFONT,fontSize:28,bold:true,color:INK});
s.addText([
  {text:"No object to look for.",options:{bullet:true,breakLine:true}},
  {text:"No answer key.",options:{bullet:true,breakLine:true}},
  {text:"And the feeling is mixed.",options:{bullet:true}},
],{x:7.3,y:3.2,w:5,h:1.8,isTextBox:true,margin:0,fontFace:BFONT,fontSize:16,
   color:MUTED,paraSpaceAfter:8});
s.addText("Nobody had built a way to check this.",
  {x:7.3,y:5.35,w:5,h:0.6,isTextBox:true,margin:0,fontFace:BFONT,fontSize:13,
   italic:true,bold:true,color:GOLD});
note(s,"Median prompt in this dataset: four words. Mixed feelings are common.");
s.addNotes("You can check 'a red car' — look for a car, check it's red. That is what the evaluation literature does. But 'tired but happy' has no object and no correct answer, and it is mixed. That gap is what this project fills.");

/* ==================================================== 3. THE DATA ========= */
s=light(); kicker(s,"The data"); titleOf(s,"A dataset that cannot be downloaded");
s.addText("Festival of the Mind 2024, Sheffield. Members of the public typed how they felt; DALL·E drew each entry as black-and-white line art.",
 {x:M,y:1.9,w:11.9,h:0.55,isTextBox:true,margin:0,fontFace:BFONT,fontSize:15,color:MUTED,valign:"top"});
statCard(s, M,    2.75, 2.7, "1,025", "drawings generated\n0 processing failures", TEAL);
statCard(s, 3.7,  2.75, 2.7, "1,012", "analysed\n(13 were pre-festival tests)", TEAL);
statCard(s, 6.7,  2.75, 2.7, "607",   "prompts carry a feeling\n405 do not — the control", GOLD);
statCard(s, 9.7,  2.75, 2.9, "87",    "prompts drawn more than once\ncovering 336 records", BLUE);
s.addShape(p.ShapeType.roundRect,{x:M,y:5.0,w:11.93,h:1.65,rectRadius:0.06,
  fill:{color:WHITE},line:{color:RULE,width:1}});
s.addText("Three traps before any analysis was possible",
  {x:M+0.35,y:5.2,w:11.2,h:0.35,isTextBox:true,margin:0,fontFace:BFONT,fontSize:14,bold:true,color:INK});
s.addText([
  {text:"Three incompatible filename schemes in one folder — a naive loader resolves under 20% of the corpus.",options:{bullet:true,breakLine:true}},
  {text:"Hidden C2PA timestamps inside every PNG revealed that records 1–13 were made before the festival.",options:{bullet:true,breakLine:true}},
  {text:"87 prompts were drawn more than once — which looked like a nuisance and became a finding.",options:{bullet:true}},
],{x:M+0.35,y:5.62,w:11.2,h:0.95,isTextBox:true,margin:0,fontFace:BFONT,fontSize:13,
   color:MUTED,paraSpaceAfter:3});
s.addNotes("Real people, real feelings, not a benchmark. Before any analysis I had to fix three filename systems, recover hidden timestamps that exposed 13 developer test images, and deal with repeated prompts.");

/* ==================================================== 4. THE GAP ========== */
s=light(); kicker(s,"The gap"); titleOf(s,"Four literatures, and the hole between them");
const gaps=[
 ["Emotion in text","Well studied. GoEmotions gives 27 categories and a classifier — but short first-person self-report is the hardest case.",GREEN],
 ["Emotional image generation","Well studied. And the strongest evidence says colour, not shape, carries most emotional meaning.",GREEN],
 ["Text-to-image evaluation","Well studied — for objects. The metrics check whether the picture contains what the prompt named.",GREEN],
 ["Reading emotion from an image","Possible but weak. Vision-language models are positively biased, order-sensitive readers.",GOLD],
];
gaps.forEach((g,i)=>{
  const y=2.05+i*0.87;
  s.addShape(p.ShapeType.ellipse,{x:M,y:y+0.09,w:0.3,h:0.3,fill:{color:g[2]},line:{type:"none"}});
  s.addText(g[0],{x:M+0.5,y:y,w:3.5,h:0.7,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:15,bold:true,color:INK,valign:"top"});
  s.addText(g[1],{x:4.3,y:y,w:8.3,h:0.7,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:13,color:MUTED,valign:"top"});
});
s.addShape(p.ShapeType.roundRect,{x:M,y:5.6,w:11.93,h:1.05,rectRadius:0.06,
  fill:{color:"E8F0EF"},line:{color:TEAL,width:1.2}});
s.addText("Nobody had asked whether the feeling in a person's own unedited words survives the journey into a drawing.",
  {x:M+0.35,y:5.7,w:11.2,h:0.85,isTextBox:true,margin:0,fontFace:HFONT,fontSize:19,
   bold:true,color:TEAL,valign:"middle"});
note(s,"97 papers collected and read · 73 kept as core evidence · organised into twelve themes");
s.addNotes("Each of these four areas is well studied on its own. What nobody had done is check whether a real person's own words about their own feeling survive into the picture.");

/* ==================================================== 5. THE QUESTION ===== */
s=dark(); kicker(s,"The research question",true);
s.addText("To what extent does an automatic image-emotion reader agree with prompt-derived emotion labels for AI-generated monochrome drawings — and how does that agreement vary by visual content and by repeated prompts?",
 {x:M,y:2.1,w:11.9,h:2.6,isTextBox:true,margin:0,fontFace:HFONT,fontSize:30,
  color:WHITE,lineSpacing:42});
s.addShape(p.ShapeType.line,{x:M,y:4.75,w:2.8,h:0,line:{color:"2F7B7F",width:1.5}});
s.addText([
  {text:"This measures agreement between two automatic systems. ",options:{bold:true}},
  {text:"It does not establish that a human viewer perceives the same feeling — and that distinction is carried honestly through every claim I make.",options:{}},
],{x:M,y:5.1,w:11.3,h:1.1,isTextBox:true,margin:0,fontFace:BFONT,fontSize:16,color:"BFD9D6"});
s.addNotes("Note how narrow this is. I measure agreement between two automatic readers. I do not claim a human sees the same feeling. Being precise about that is the difference between a defensible claim and an overclaim.");

/* ==================================================== 6. METHOD =========== */
s=light(); kicker(s,"Method"); titleOf(s,"Describe first. Never ask for the emotion.");
const steps=[
 ["01","Describe","Five plain factual questions to the image model: expression, action, posture, how many people, what is in the picture.",TEAL],
 ["02","Read","A separate language model infers a feeling from that description. A third model reads the person's own words.",GOLD],
 ["03","Compare","Four measures of closeness — every one referenced to chance.",BLUE],
];
steps.forEach((st,i)=>{
  const x=M+i*4.05;
  s.addShape(p.ShapeType.roundRect,{x:x,y:2.05,w:3.75,h:2.7,rectRadius:0.06,
    fill:{color:WHITE},line:{color:RULE,width:1}});
  s.addShape(p.ShapeType.ellipse,{x:x+0.35,y:2.4,w:0.6,h:0.6,fill:{color:st[3]},line:{type:"none"}});
  s.addText(st[0],{x:x+0.35,y:2.4,w:0.6,h:0.6,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:15,bold:true,color:WHITE,align:"center",valign:"middle"});
  s.addText(st[1],{x:x+1.1,y:2.45,w:2.4,h:0.5,isTextBox:true,margin:0,fontFace:HFONT,
    fontSize:22,bold:true,color:INK,valign:"middle"});
  s.addText(st[2],{x:x+0.35,y:3.25,w:3.05,h:1.35,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:13,color:MUTED,valign:"top"});
});
s.addShape(p.ShapeType.roundRect,{x:M,y:5.15,w:11.93,h:1.3,rectRadius:0.06,
  fill:{color:"FBF3E7"},line:{color:GOLD,width:1.2}});
s.addText("The vision model is never asked “what emotion is this?” — that is the supervisor's design, and it is measurably better.",
  {x:M+0.35,y:5.35,w:11.2,h:0.9,isTextBox:true,margin:0,fontFace:HFONT,fontSize:18,
   bold:true,color:INK,valign:"middle"});
s.addNotes("The architecture my supervisor specified: describe the picture factually first, then infer the feeling from that description with a different model. The word emotion never appears in any question I ask the image.");

/* ==================================================== 7. THE 5 QUESTIONS == */
s=light(); kicker(s,"Method · stage one"); titleOf(s,"The five questions asked of every drawing");
const qs=["What is the facial expression?","What is the person doing?","What is the body posture?",
          "How many people are there?","What is in the picture?"];
qs.forEach((q,i)=>{
  const y=2.05+i*0.78;
  s.addShape(p.ShapeType.roundRect,{x:M,y:y,w:7.4,h:0.58,rectRadius:0.05,
    fill:{color:WHITE},line:{color:RULE,width:1}});
  s.addText(String(i+1),{x:M+0.2,y:y,w:0.4,h:0.58,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:13,bold:true,color:TEAL,align:"center",valign:"middle"});
  s.addText(q,{x:M+0.7,y:y,w:6.5,h:0.58,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:15,color:INK,valign:"middle"});
});
s.addShape(p.ShapeType.roundRect,{x:8.5,y:2.05,w:4.13,h:3.55,rectRadius:0.06,
  fill:{color:"E8F0EF"},line:{color:TEAL,width:1.2}});
s.addText("Then, one neutral sentence",{x:8.8,y:2.25,w:3.6,h:0.4,isTextBox:true,margin:0,
  fontFace:BFONT,fontSize:13,bold:true,color:TEAL});
s.addText("“A drawing of one person showing a park. The person is sitting, hunched. The facial expression is sad.”",
  {x:8.8,y:2.68,w:3.6,h:1.65,isTextBox:true,margin:0,fontFace:HFONT,fontSize:15,
   italic:true,color:INK});
s.addText("A second model reads a feeling out of that sentence — never out of the picture.",
  {x:8.8,y:4.38,w:3.6,h:1.05,isTextBox:true,margin:0,fontFace:BFONT,fontSize:12,color:MUTED,valign:"top"});
note(s,"Honest caveat: the expression answer is often already a feeling word, so the two stages are not fully independent. This is reported.");
s.addNotes("These are the exact five questions. The answers are assembled into one neutral sentence, and a separate model reads the feeling from that sentence. I flag openly that the expression answer is often itself a feeling word, so the stages are not fully independent.");

/* ==================================================== 8. REJECTED ========= */
s=light(); kicker(s,"Method development"); titleOf(s,"Four things that failed first");
const rows=[
 ["GoEmotions on the descriptions","Collapsed to “neutral” above 95%. It needs first-person feeling words; a visual description has none."],
 ["A single image caption","Too terse — “a man with hands in the air”. The reader collapsed to “surprise” for almost everything."],
 ["Qwen2.5-VL, 3B parameters","Exceeded a 16 GB laptop. Thrashed into swap: 4 hours 45 minutes, zero progress."],
 ["Asking CLIP for the emotion","Beaten head-to-head — and inspection found arms-raised celebration read as anger, 0.73."],
];
rows.forEach((r,i)=>{
  const y=2.05+i*0.99;
  s.addShape(p.ShapeType.roundRect,{x:M,y:y,w:11.93,h:0.8,rectRadius:0.05,
    fill:{color:WHITE},line:{color:RULE,width:1}});
  s.addText("✕",{x:M+0.25,y:y,w:0.45,h:0.8,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:17,bold:true,color:RED,align:"center",valign:"middle"});
  s.addText(r[0],{x:M+0.85,y:y,w:3.5,h:0.8,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:14,bold:true,color:INK,valign:"middle"});
  s.addText(r[1],{x:M+4.5,y:y,w:7.2,h:0.8,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:13,color:MUTED,valign:"middle"});
});
s.addShape(p.ShapeType.roundRect,{x:M,y:6.0,w:11.93,h:0.8,rectRadius:0.05,
  fill:{color:"E8F0EF"},line:{color:TEAL,width:1.4}});
s.addText("✓",{x:M+0.25,y:6.0,w:0.45,h:0.8,isTextBox:true,margin:0,fontFace:BFONT,
  fontSize:17,bold:true,color:TEAL,align:"center",valign:"middle"});
s.addText("BLIP-VQA",{x:M+0.85,y:6.0,w:3.5,h:0.8,isTextBox:true,margin:0,fontFace:BFONT,
  fontSize:14,bold:true,color:TEAL,valign:"middle"});
s.addText("0.4B parameters, ~1.5 s per drawing — and its “facial expression” answer is exactly the cue the next stage needs.",
  {x:M+4.5,y:6.0,w:7.2,h:0.8,isTextBox:true,margin:0,fontFace:BFONT,fontSize:13,
   color:TEAL,valign:"middle"});
s.addNotes("Each link was tested before I trusted it. These failures shaped the design and are findings in their own right — especially the memory limit, which is why the final design is constrained by what actually runs on the hardware I had.");

/* ==================================================== 9. NULLS ============ */
s=light(); kicker(s,"Rigour"); titleOf(s,"Every number is measured against luck");
s.addText("Within each subset, the drawings are shuffled and re-paired against the untouched prompts, and all four measures are recomputed. Repeated 300 times, with a fixed seed.",
 {x:M,y:1.9,w:11.9,h:0.7,isTextBox:true,margin:0,fontFace:BFONT,fontSize:16,color:MUTED,valign:"top"});
// visual: real pairing vs shuffled pairing
s.addShape(p.ShapeType.roundRect,{x:M,y:2.75,w:5.75,h:2.75,rectRadius:0.06,
  fill:{color:WHITE},line:{color:TEAL,width:1.2}});
s.addText("Real pairing",{x:M+0.35,y:2.98,w:5,h:0.4,isTextBox:true,margin:0,
  fontFace:BFONT,fontSize:14,bold:true,color:TEAL});
[0,1,2].forEach(i=>{ motif(s, M+0.75, 3.62+i*0.52, 0.1, TEAL, TEAL, 4.4); });
s.addText("each drawing with its own words",{x:M+0.35,y:5.05,w:5,h:0.35,isTextBox:true,
  margin:0,fontFace:BFONT,fontSize:12,italic:true,color:MUTED});

s.addShape(p.ShapeType.roundRect,{x:6.9,y:2.75,w:5.75,h:2.75,rectRadius:0.06,
  fill:{color:WHITE},line:{color:RULE,width:1}});
s.addText("Shuffled — 300 times",{x:7.25,y:2.98,w:5,h:0.4,isTextBox:true,margin:0,
  fontFace:BFONT,fontSize:14,bold:true,color:MUTED});
[0,1,2].forEach(i=>{ motif(s, 7.65, 3.62+i*0.52, 0.1, "8A9096", "8A9096", 4.4); });
s.addText("each drawing with a stranger's words",{x:7.25,y:5.05,w:5,h:0.35,isTextBox:true,
  margin:0,fontFace:BFONT,fontSize:12,italic:true,color:MUTED});

s.addShape(p.ShapeType.roundRect,{x:M,y:5.88,w:11.93,h:0.95,rectRadius:0.06,
  fill:{color:"E8F0EF"},line:{color:TEAL,width:1.2}});
s.addText("A result counts only insofar as it beats the shuffle. Every figure in this talk is quoted against its own null.",
  {x:M+0.35,y:5.98,w:11.2,h:0.75,isTextBox:true,margin:0,fontFace:HFONT,fontSize:18,
   bold:true,color:TEAL,valign:"middle"});
s.addNotes("This is the backbone of the whole evaluation. I never report a raw percentage. I always report it against what pure chance gives on the same data.");

/* ==================================================== 10. CONTROL ========= */
s=dark(); kicker(s,"Rigour · the validity check",true);
titleOf(s,"A control that passes",true);
s.addText("405 of the 1,012 prompts contain no feeling at all.",
 {x:M,y:1.9,w:11.9,h:0.5,isTextBox:true,margin:0,fontFace:BFONT,fontSize:17,color:"BFD9D6"});
["“pigs”","“mickey mouse”","“disney characters”"].forEach((t,i)=>{
  s.addShape(p.ShapeType.roundRect,{x:M+i*2.9,y:2.6,w:2.65,h:0.85,rectRadius:0.06,
    fill:{color:"0E4145"},line:{color:"2F7B7F",width:1}});
  s.addText(t,{x:M+i*2.9,y:2.6,w:2.65,h:0.85,isTextBox:true,margin:0,fontFace:HFONT,
    fontSize:19,italic:true,color:WHITE,align:"center",valign:"middle"});
});
s.addText("If my method were inventing emotion, it would score above chance here.",
 {x:M,y:3.75,w:11.9,h:0.45,isTextBox:true,margin:0,fontFace:BFONT,fontSize:16,color:"BFD9D6"});
s.addShape(p.ShapeType.roundRect,{x:M,y:4.42,w:11.93,h:1.5,rectRadius:0.06,
  fill:{color:"0E4145"},line:{color:"3FA39B",width:1.4}});
s.addText("76.6%",{x:M+0.4,y:4.57,w:2.6,h:1.2,isTextBox:true,margin:0,fontFace:HFONT,
  fontSize:40,bold:true,color:WHITE,valign:"middle"});
s.addText("measured",{x:M+3.0,y:4.57,w:1.8,h:1.2,isTextBox:true,margin:0,fontFace:BFONT,
  fontSize:13,color:"9FB4B3",valign:"middle"});
s.addText("76.6%",{x:M+4.6,y:4.57,w:2.6,h:1.2,isTextBox:true,margin:0,fontFace:HFONT,
  fontSize:40,bold:true,color:"7FC4BE",valign:"middle"});
s.addText("pure chance",{x:M+7.2,y:4.57,w:2.0,h:1.2,isTextBox:true,margin:0,fontFace:BFONT,
  fontSize:13,color:"9FB4B3",valign:"middle"});
s.addText("z = +0.3",{x:M+9.2,y:4.57,w:2.3,h:1.2,isTextBox:true,margin:0,fontFace:HFONT,
  fontSize:28,bold:true,color:"7FC4BE",align:"right",valign:"middle"});
s.addText("It finds emotion only where emotion exists. That is why the other numbers can be believed.",
 {x:M,y:6.2,w:11.9,h:0.6,isTextBox:true,margin:0,fontFace:HFONT,fontSize:20,bold:true,color:WHITE});
s.addNotes("This is the slide I would most like you to remember. Four hundred people typed things with no feeling in them. On those, my method scores exactly what luck scores. An instrument that reports a signal where there is none cannot be trusted anywhere — mine does not.");

/* ==================================================== 11. CHANCE ========== */
s=dark(); kicker(s,"Rigour · calibrating the scale",true);
titleOf(s,"Chance is not zero",true);
s.addText("The similarity measure cannot reach 0 — and randomly paired items already score 76.",
 {x:M,y:1.9,w:11.9,h:0.5,isTextBox:true,margin:0,fontFace:BFONT,fontSize:17,color:"BFD9D6"});
// ruler: 41 -> 100 mapped onto 11.93 inches
const RX=M, RY=3.0, RW=11.93;
const at = v => RX + ((v-41)/(100-41))*RW;
s.addShape(p.ShapeType.roundRect,{x:RX,y:RY,w:RW,h:0.62,rectRadius:0.08,
  fill:{color:"0E4145"},line:{color:"2F7B7F",width:1}});
s.addShape(p.ShapeType.rect,{x:RX,y:RY,w:at(76)-RX,h:0.62,fill:{color:"1B5F5B"},line:{type:"none"}});
s.addShape(p.ShapeType.rect,{x:RX,y:RY-0.18,w:0.035,h:0.98,fill:{color:"9FB4B3"},line:{type:"none"}});
s.addShape(p.ShapeType.rect,{x:at(76),y:RY-0.18,w:0.035,h:0.98,fill:{color:WHITE},line:{type:"none"}});
s.addShape(p.ShapeType.rect,{x:at(84),y:RY-0.18,w:0.05,h:0.98,fill:{color:"F0B040"},line:{type:"none"}});
[[41,"41\nfloor — impossible to go lower","9FB4B3","left"],
 [76,"76\nrandom pairings","FFFFFF","center"],
 [84,"84\nmy result","F0B040","center"]].forEach(t=>{
  const x = t[0]===41 ? RX-0.05 : at(t[0])-1.3;
  s.addText(t[1],{x:x,y:RY+0.78,w:2.6,h:0.85,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:13,bold:true,color:t[2],align:t[3]});
});
s.addShape(p.ShapeType.roundRect,{x:M,y:5.15,w:5.85,h:1.55,rectRadius:0.06,
  fill:{color:"0E4145"},line:{color:"9E3B33",width:1.4}});
s.addText("A score of 71 looks like a pass.\nIt is below chance.",
  {x:M+0.35,y:5.32,w:5.2,h:1.25,isTextBox:true,margin:0,fontFace:HFONT,fontSize:20,
   bold:true,color:"F09490",valign:"middle"});
s.addShape(p.ShapeType.roundRect,{x:6.85,y:5.15,w:5.78,h:1.55,rectRadius:0.06,
  fill:{color:"0E4145"},line:{color:"2F7B7F",width:1}});
s.addText("So I changed what I report: mood-direction and emotion-family agreement now lead, and this score is always shown against its chance line.",
  {x:7.2,y:5.32,w:5.1,h:1.25,isTextBox:true,margin:0,fontFace:BFONT,fontSize:14,
   color:"BFD9D6",valign:"middle"});
s.addNotes("I found this late and it changed how I report everything. This measure has a floor of 41 and random pairs already score 76. So a 71 looks like a pass but is worse than luck. It also gives about the same value for faces and scenes, so it cannot discriminate — which is why I promoted the other two measures to the headline.");

/* ==================================================== 12. FINDING 1 ======= */
s=light(); kicker(s,"Finding one"); titleOf(s,"Alignment is far stronger when there is a face");
s.addChart(p.ChartType.bar,[
  {name:"Face drawings (n=402)", labels:["Mood direction","Emotion family","Top-3 overlap"], values:[73.9,61.9,53.4]},
  {name:"Scene drawings (n=205)",labels:["Mood direction","Emotion family","Top-3 overlap"], values:[42.9,35.6,44.9]},
],{x:M,y:1.95,w:7.6,h:4.55,barDir:"col",chartColors:[TEAL,"C9BFA8"],
   showTitle:false,showLegend:true,legendPos:"b",legendFontFace:BFONT,legendFontSize:12,
   showValue:true,dataLabelPosition:"outEnd",dataLabelFormatCode:'0.0"%"',
   dataLabelFontFace:BFONT,dataLabelFontSize:11,dataLabelColor:INK,
   catAxisLabelFontFace:BFONT,catAxisLabelFontSize:12,catAxisLabelColor:MUTED,
   valAxisLabelFontFace:BFONT,valAxisLabelFontSize:11,valAxisLabelColor:MUTED,
   valAxisMaxVal:85,valAxisMinVal:0,valGridLine:{color:"E5E1DA",size:1},
   catGridLine:{style:"none"},barGapWidthPct:55});
s.addShape(p.ShapeType.roundRect,{x:8.55,y:1.95,w:4.08,h:1.95,rectRadius:0.06,
  fill:{color:WHITE},line:{color:RULE,width:1}});
s.addText("1.7×",{x:8.85,y:2.12,w:3.5,h:0.75,isTextBox:true,margin:0,fontFace:HFONT,
  fontSize:44,bold:true,color:TEAL});
s.addText("better alignment on both mood direction and emotion family",
  {x:8.85,y:2.95,w:3.5,h:0.85,isTextBox:true,margin:0,fontFace:BFONT,fontSize:13,color:MUTED,valign:"top"});
s.addShape(p.ShapeType.roundRect,{x:8.55,y:4.35,w:4.08,h:2.15,rectRadius:0.06,
  fill:{color:"FBF3E7"},line:{color:GOLD,width:1}});
s.addText("Stated carefully",{x:8.85,y:4.55,w:3.5,h:0.35,isTextBox:true,margin:0,
  fontFace:BFONT,fontSize:13,bold:true,color:GOLD});
s.addText("The pipeline finds stronger alignment for drawings it classifies as containing a readable face. That classification and the emotion reading share a source — so this is partly circular, and I say so.",
  {x:8.85,y:4.95,w:3.5,h:1.45,isTextBox:true,margin:0,fontFace:BFONT,fontSize:12,color:MUTED,valign:"top"});
note(s,"All above chance (z +4.4 to +10.4). Holds on distinct prompts only: face 71.8% vs scene 37.3%.");
s.addNotes("This is the headline finding. Note the careful wording — I do not say faces carry emotion. I say the pipeline finds stronger alignment for drawings it classifies as containing a face, and I flag that the classification and the emotion reading share a source.");

/* ==================================================== 13. FINDING 2 ======= */
s=light(); kicker(s,"Finding two"); titleOf(s,"The generator is inconsistent with itself");
s.addText("87 prompts were drawn between 2 and 42 times each. Same words in — different feeling out.",
 {x:M,y:1.9,w:11.9,h:0.5,isTextBox:true,margin:0,fontFace:BFONT,fontSize:16,color:MUTED,valign:"top"});
const c13=cols(3,3.6);
statCard(s, c13[0], 2.75, 3.6, "68.8%", "of the time the redrawn image conveys the SAME emotion", BLUE);
statCard(s, c13[1], 2.75, 3.6, "28 / 87", "repeated prompts are fully consistent across all their drawings", GOLD);
statCard(s, c13[2], 2.75, 3.6, "336", "records sit inside a repeated-prompt group", TEAL);
s.addShape(p.ShapeType.roundRect,{x:M,y:5.1,w:11.93,h:1.65,rectRadius:0.06,
  fill:{color:"E8F0EF"},line:{color:TEAL,width:1.2}});
s.addText("A single drawing is one sample of the model's behaviour — not a fixed answer.",
  {x:M+0.35,y:5.3,w:11.2,h:0.5,isTextBox:true,margin:0,fontFace:HFONT,fontSize:21,
   bold:true,color:TEAL});
s.addText("That is a caution for anyone evaluating a generative model on a single output — including the standard benchmarks.",
  {x:M+0.35,y:5.9,w:11.2,h:0.7,isTextBox:true,margin:0,fontFace:BFONT,fontSize:14,color:MUTED});
s.addNotes("This one surprised me. Give the model exactly the same words again and it conveys the same emotion only about seven times in ten. Only 28 of the 87 repeated prompts are fully consistent. So evaluating a generator on one output per prompt is not safe.");

/* ==================================================== 14. FINDING 3 ======= */
s=light(); kicker(s,"Finding three"); titleOf(s,"The architecture choice was worth 24 points");
s.addChart(p.ChartType.bar,[
  {name:"Describe → extract (this project)", labels:["Emotion family","Top-3 overlap"], values:[49.3,48.6]},
  {name:"Ask CLIP directly (baseline)",      labels:["Emotion family","Top-3 overlap"], values:[25.3,22.8]},
],{x:M,y:1.95,w:7.6,h:4.75,barDir:"col",chartColors:[TEAL,"C9BFA8"],
   showTitle:false,showLegend:true,legendPos:"b",legendFontFace:BFONT,legendFontSize:12,
   showValue:true,dataLabelPosition:"outEnd",dataLabelFormatCode:'0.0"%"',
   dataLabelFontFace:BFONT,dataLabelFontSize:11,dataLabelColor:INK,
   catAxisLabelFontFace:BFONT,catAxisLabelFontSize:12,catAxisLabelColor:MUTED,
   valAxisLabelFontFace:BFONT,valAxisLabelFontSize:11,valAxisLabelColor:MUTED,
   valAxisMaxVal:60,valAxisMinVal:0,valGridLine:{color:"E5E1DA",size:1},
   catGridLine:{style:"none"},barGapWidthPct:60});
s.addText("Head-to-head on the same records, with the prompt side held constant and only the image reader changed.",
  {x:8.55,y:1.98,w:4.08,h:1.1,isTextBox:true,margin:0,fontFace:BFONT,fontSize:14,color:MUTED,valign:"top"});
s.addShape(p.ShapeType.roundRect,{x:8.55,y:3.25,w:4.08,h:1.65,rectRadius:0.06,
  fill:{color:"E8F0EF"},line:{color:TEAL,width:1.2}});
s.addText("Roughly double",{x:8.85,y:3.42,w:3.5,h:0.45,isTextBox:true,margin:0,
  fontFace:HFONT,fontSize:24,bold:true,color:TEAL});
s.addText("So the supervisor's redirection was empirically justified, not simply accepted. Asking a vision model for an emotion directly performs poorly on line art.",
  {x:8.85,y:3.88,w:3.5,h:0.9,isTextBox:true,margin:0,fontFace:BFONT,fontSize:12.5,color:MUTED,valign:"top"});
s.addShape(p.ShapeType.roundRect,{x:8.55,y:5.1,w:4.08,h:1.6,rectRadius:0.06,
  fill:{color:WHITE},line:{color:RULE,width:1}});
s.addText("83.7% vs 74.2%",{x:8.85,y:5.28,w:3.5,h:0.5,isTextBox:true,margin:0,
  fontFace:HFONT,fontSize:22,bold:true,color:INK});
s.addText("on valence–arousal similarity — the measure that cannot separate faces from scenes",
  {x:8.85,y:5.8,w:3.5,h:0.8,isTextBox:true,margin:0,fontFace:BFONT,fontSize:12,color:MUTED,valign:"top"});
s.addNotes("I did not just accept the architecture — I measured it. Describe-then-extract roughly doubles emotion-family agreement against asking CLIP directly, on the same records.");

/* ==================================================== 15. DEMO ============ */
s=light(); kicker(s,"Built alongside"); titleOf(s,"A live instrument, not a screenshot");
s.addText("The pipeline runs in a browser: pick a drawing or upload one, watch the five answers appear, see both readings side by side, and see the similarity scored against chance.",
 {x:M,y:1.9,w:11.9,h:0.65,isTextBox:true,margin:0,fontFace:BFONT,fontSize:16,color:MUTED,valign:"top"});
const demo=[["Choose a drawing","from the dataset, or upload your own image"],
            ["Watch it described","five factual answers — emotion never asked"],
            ["Compare","both readings, and the score against chance"]];
demo.forEach((d,i)=>{
  const x=M+i*4.05;
  s.addShape(p.ShapeType.roundRect,{x:x,y:2.75,w:3.75,h:1.9,rectRadius:0.06,
    fill:{color:WHITE},line:{color:RULE,width:1}});
  s.addText(d[0],{x:x+0.3,y:2.98,w:3.15,h:0.4,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:15,bold:true,color:TEAL});
  s.addText(d[1],{x:x+0.3,y:3.45,w:3.15,h:1.05,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:13,color:MUTED,valign:"top"});
});
s.addShape(p.ShapeType.roundRect,{x:M,y:4.95,w:11.93,h:1.8,rectRadius:0.06,
  fill:{color:"E8F0EF"},line:{color:TEAL,width:1.2}});
s.addText("Every number it shows is referenced to chance",{x:M+0.4,y:5.12,w:11.1,h:0.4,
  isTextBox:true,margin:0,fontFace:BFONT,fontSize:15,bold:true,color:TEAL});
s.addText([
  {text:"the axis starts at the measure's real floor of 41, not at 0",options:{bullet:true,breakLine:true}},
  {text:"the middle half of random pairings is bracketed on the scale",options:{bullet:true,breakLine:true}},
  {text:"the headline reads “closer than N% of random pairings”",options:{bullet:true,breakLine:true}},
  {text:"nothing typed or uploaded is stored, and no visitor IP is logged",options:{bullet:true}},
],{x:M+0.4,y:5.52,w:11.1,h:1.15,isTextBox:true,margin:0,fontFace:BFONT,fontSize:13,
   color:MUTED,paraSpaceAfter:2});
s.addNotes("I will show this live if there is time. The point of the demo is that the method is inspectable — you can watch it describe a drawing and see exactly where the emotion reading comes from.");

/* ==================================================== 16. ETHICS ========== */
s=light(); kicker(s,"Data protection"); titleOf(s,"Redacting names without breaking the data");
s.addText("Supervisor's direction: redact real names, keep illness and grief content — it is not identifying on its own and it is essential to the analysis — and document the procedure.",
 {x:M,y:1.9,w:11.9,h:0.65,isTextBox:true,margin:0,fontFace:BFONT,fontSize:15,color:MUTED,valign:"top"});
const eth=[["Detect","77% of the corpus is lower case, so capitals alone would miss most names. A 7,944-name gazetteer, a 236,000-word dictionary, and naming phrases.",TEAL],
           ["Review","Every candidate carries a recorded decision and a reason. The audit fails if anything is unreviewed.",GOLD],
           ["Apply","Scoped to the specific record each name was reviewed in.",BLUE]];
eth.forEach((e,i)=>{
  const x=M+i*4.05;
  s.addShape(p.ShapeType.roundRect,{x:x,y:2.75,w:3.75,h:2.05,rectRadius:0.06,
    fill:{color:WHITE},line:{color:RULE,width:1}});
  s.addShape(p.ShapeType.ellipse,{x:x+0.3,y:2.95,w:0.42,h:0.42,fill:{color:e[2]},line:{type:"none"}});
  s.addText(String(i+1),{x:x+0.3,y:2.95,w:0.42,h:0.42,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:12,bold:true,color:WHITE,align:"center",valign:"middle"});
  s.addText(e[0],{x:x+0.85,y:2.95,w:2.6,h:0.42,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:16,bold:true,color:INK,valign:"middle"});
  s.addText(e[1],{x:x+0.3,y:3.52,w:3.15,h:1.2,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:12,color:MUTED,valign:"top"});
});
s.addShape(p.ShapeType.roundRect,{x:M,y:5.18,w:5.85,h:1.6,rectRadius:0.06,
  fill:{color:"FBF3E7"},line:{color:GOLD,width:1}});
s.addText("Two errors the audit caught",{x:M+0.35,y:5.33,w:5.2,h:0.35,isTextBox:true,
  margin:0,fontFace:BFONT,fontSize:14,bold:true,color:GOLD});
s.addText([
  {text:"A bare name list destroyed “Jack Frost” and “woolly mammoth”.",options:{bullet:true,breakLine:true}},
  {text:"Redaction forged a duplicate: two different names both became [name].",options:{bullet:true}},
],{x:M+0.35,y:5.7,w:5.2,h:1.0,isTextBox:true,margin:0,fontFace:BFONT,fontSize:12,
   color:MUTED,paraSpaceAfter:3});
s.addShape(p.ShapeType.roundRect,{x:6.85,y:5.18,w:5.78,h:1.6,rectRadius:0.06,
  fill:{color:"E8F0EF"},line:{color:TEAL,width:1.2}});
s.addText("Redaction is analytically inert",{x:7.2,y:5.33,w:5.1,h:0.35,isTextBox:true,
  margin:0,fontFace:BFONT,fontSize:14,bold:true,color:TEAL});
s.addText("Re-running the text model on the redacted prompts moves each probability by at most 0.012 and changes zero emotion readings. 8 records held names; all 1,012 are still shown.",
  {x:7.2,y:5.7,w:5.1,h:1.0,isTextBox:true,margin:0,fontFace:BFONT,fontSize:12,color:MUTED,valign:"top"});
s.addNotes("No participants and no new data, so no ethics approval was required. But the dataset contains real names, so I built a documented redaction procedure — and proved it does not change any result.");

/* ==================================================== 17. LIMITS ========== */
s=light(); kicker(s,"Honesty"); titleOf(s,"What I cannot claim");
const lims=[
 ["This is automated agreement, not human perception","Both readers are models and they disagree in opposite directions: CLIP skews negative on line art, the description model reads 57% of readable faces as happy.",RED],
 ["The face / scene split is partly circular","It is defined by whether the model reported an expression — and the emotion is read from that same description.",GOLD],
 ["The valence–arousal score is a designed proxy","Built on hand-set emotion coordinates. Not a continuous lexicon rating, and it cannot separate faces from scenes.",GOLD],
 ["No claim about colour, and none about direction","The corpus is monochrome but there is no colour condition. An earlier positive-versus-negative claim was withdrawn.",MUTED],
];
lims.forEach((l,i)=>{
  const y=2.0+i*1.17;
  s.addShape(p.ShapeType.roundRect,{x:M,y:y,w:11.93,h:1.0,rectRadius:0.05,
    fill:{color:WHITE},line:{color:RULE,width:1}});
  s.addShape(p.ShapeType.ellipse,{x:M+0.3,y:y+0.33,w:0.32,h:0.32,fill:{color:l[2]},line:{type:"none"}});
  s.addText(l[0],{x:M+0.85,y:y+0.12,w:4.6,h:0.78,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:14,bold:true,color:INK,valign:"middle"});
  s.addText(l[1],{x:M+5.7,y:y+0.12,w:6.0,h:0.78,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:12.5,color:MUTED,valign:"middle"});
});
note(s,"A human-rating study was designed in full and deliberately not run — approval alone would have taken a fortnight. It is the clear next step.");
s.addNotes("I want to state these before anyone asks. The most important one is the first: I measure agreement between two models, not human perception. Only human ratings could settle that, and that study is designed and ready but was not run.");

/* ==================================================== 18. CONTRIBUTION ==== */
s=dark(); kicker(s,"In summary",true); titleOf(s,"What this contributes",true);
s.addText("Not a novel emotion classifier.",{x:M,y:1.5,w:11.9,h:0.45,isTextBox:true,
  margin:0,fontFace:BFONT,fontSize:17,italic:true,color:"9FB4B3"});
const contrib=[
 ["A question nobody had asked","of real, first-person, mixed self-report"],
 ["A dataset that cannot be downloaded","1,025 real emotional entries with their drawings"],
 ["An evaluation design that holds up","null baselines throughout, and a control that passes"],
 ["A measured method comparison","the architecture was justified, not assumed"],
 ["A generative-consistency finding","the same prompt does not convey the same feeling"],
 ["A documented data-protection procedure","tested, and proven not to change any result"],
];
contrib.forEach((c,i)=>{
  const x = M + (i%2)*6.05, y = 2.45 + Math.floor(i/2)*1.15;
  s.addShape(p.ShapeType.ellipse,{x:x,y:y+0.1,w:0.26,h:0.26,fill:{color:"7FC4BE"},line:{type:"none"}});
  s.addText(c[0],{x:x+0.45,y:y,w:5.4,h:0.42,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:15,bold:true,color:WHITE});
  s.addText(c[1],{x:x+0.45,y:y+0.42,w:5.4,h:0.55,isTextBox:true,margin:0,fontFace:BFONT,
    fontSize:13,color:"9FB4B3"});
});
s.addShape(p.ShapeType.line,{x:M,y:5.85,w:11.93,h:0,line:{color:"2F7B7F",width:1}});
s.addText("Thank you — questions welcome",{x:M,y:6.1,w:7,h:0.5,isTextBox:true,margin:0,
  fontFace:HFONT,fontSize:22,bold:true,color:WHITE});
s.addText("Next step: human validation of the automatic readers",{x:7.7,y:6.15,w:4.9,h:0.45,
  isTextBox:true,margin:0,fontFace:BFONT,fontSize:13,italic:true,color:"7FC4BE",align:"right"});
s.addNotes("To summarise: the contribution is not a new model. It is the question, the dataset, an evaluation design with a working control, a measured method comparison, the consistency finding, and a documented redaction procedure. Thank you.");

p.writeFile({fileName:"Visualising_Emotion.pptx"}).then(f=>console.log("written:",f));
