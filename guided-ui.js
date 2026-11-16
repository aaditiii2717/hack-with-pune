/* Context-aware journey cues for first-time users. */
(() => {
  const style=document.createElement("style");
  style.textContent=""+
    ".canvas,.main{font-size:14px}.canvas .button,.main .button,.canvas .tabs button,.main .tabs button,.canvas .nav button,.main .nav button{font-size:13px!important}"+
    ".card-head h2,.head h2{font-size:16px!important}.card-head p,.head p,.note,.h-meta,.template small,.small,.source small,.item small{font-size:13px!important}"+
    ".field-top b,.fieldhead b,.fieldhead .badge,.field-content,.field-content textarea,.fieldbody textarea,.citation,.citation a,.cite,.answer,.question p{font-size:14px!important}"+
    ".field label,.form label,.form input,.form select,.form textarea,.qa textarea{font-size:14px!important}.crumb,.kicker,.eyebrow,.profile small{font-size:12px!important}"+
    ".kc-guide{background:#fff;border:1px solid #e9e6e4;border-radius:11px;padding:16px;margin:0 0 16px;color:#242123}"+
    ".kc-guide h2{font:700 16px Manrope,sans-serif;margin:0 0 5px}.kc-guide p{font:400 14px/1.5 'DM Sans',sans-serif;color:#797479;margin:0}"+
    ".kc-guide-head{display:flex;justify-content:space-between;align-items:flex-start;gap:14px}.kc-guide-next{border:0;border-radius:7px;background:#7c0919;color:white;padding:10px 13px;font:700 13px 'DM Sans',sans-serif;cursor:pointer}"+
    ".kc-guide-steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-top:13px}.kc-guide-step{border:1px solid #e9e6e4;border-radius:8px;padding:10px;font:400 12px/1.45 'DM Sans',sans-serif;color:#797479}"+
    ".kc-guide-step b{display:block;color:#242123;font-size:13px;margin-bottom:3px}.kc-guide-step.done{background:#f1f7f3;border-color:#d7e8dc}.kc-guide-step.current{background:#fff7eb;border-color:#ead5ab}"+
    ".kc-chain{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));margin-top:14px;border:1px solid #e9e6e4;border-radius:9px;overflow:hidden}.kc-chain-stage{position:relative;padding:10px 12px;background:#fff;border-right:1px solid #e9e6e4;min-width:0}.kc-chain-stage:last-child{border-right:0}.kc-chain-stage b{display:block;font:700 12px/1.35 Manrope,sans-serif;color:#242123}.kc-chain-stage span{display:block;margin-top:4px;font:400 12px/1.4 'DM Sans',sans-serif;color:#797479;overflow-wrap:anywhere}.kc-chain-stage small{display:block;margin-top:7px;font:700 10px/1.3 'DM Sans',sans-serif;color:#797479;text-transform:uppercase;letter-spacing:.45px}.kc-chain-stage.done{background:#f1f7f3}.kc-chain-stage.done small{color:#2e7355}.kc-chain-stage.current{background:#fff7eb}.kc-chain-stage.current small{color:#96631b}.kc-chain-stage.waiting small{color:#797479}"+
    ".kc-guide-link{border:0;background:none;padding:0;color:#7c0919;font:700 12px 'DM Sans',sans-serif;text-decoration:underline;cursor:pointer}"+
    "@media(max-width:760px){.kc-guide-head{flex-direction:column}.kc-guide-next{width:100%}.kc-guide-steps{grid-template-columns:1fr 1fr}.kc-chain{grid-template-columns:1fr 1fr}.kc-chain-stage:nth-child(2){border-right:0}.kc-chain-stage:nth-child(-n+2){border-bottom:1px solid #e9e6e4}}@media(max-width:430px){.kc-guide-steps,.kc-chain{grid-template-columns:1fr}.kc-chain-stage{border-right:0;border-bottom:1px solid #e9e6e4}.kc-chain-stage:last-child{border-bottom:0}}";
  document.head.appendChild(style);
  const link=(label,action)=>{const b=document.createElement("button");b.type="button";b.className="kc-guide-link";b.textContent=label;b.onclick=action;return b;};
  const step=(box,title,description,state,label,action)=>{const d=document.createElement("div");d.className="kc-guide-step "+(state||"");const b=document.createElement("b");b.textContent=title;const s=document.createElement("span");s.textContent=description;d.append(b,s);if(label){d.append(document.createElement("br"),link(label,action));}box.append(d);};
  function mount(root,tabs,guide){if(root&&!root.querySelector(".kc-guide")&&tabs)root.insertBefore(guide,tabs);}
  function guideBase(title,description){const g=document.createElement("section");g.className="kc-guide";g.setAttribute("aria-label","Guided handover steps");const h=document.createElement("div");h.className="kc-guide-head";const text=document.createElement("div"),t=document.createElement("h2"),p=document.createElement("p");t.textContent=title;p.textContent=description;text.append(t,p);h.append(text);g.append(h);return {g,h};}
  function responsibilityChain(root,h){
    if(!root||!h)return;
    const status=h.status||"Draft",submitted=["Submitted","In review","Published"].includes(status),published=status==="Published",acknowledged=Boolean(h.acknowledged_at);
    const stages=[
      {title:"1 · Senior owner",name:h.owner||"Project owner",detail:"Sets the template and assigns the handover",state:"done"},
      {title:"2 · Builder",name:h.departing_person||"Departing teammate",detail:"Adds evidence, completes fields, answers gaps",state:submitted?"done":"current"},
      {title:"3 · Senior review",name:h.owner||"Project owner",detail:"Checks citations, approves, controls sharing",state:published?"done":submitted?"current":"waiting"},
      {title:"4 · Incoming engineer",name:h.recipient||"Incoming teammate",detail:"Reads approved context and confirms receipt",state:acknowledged?"done":published?"current":"waiting"}
    ];
    const chain=document.createElement("div");chain.className="kc-chain";chain.setAttribute("role","list");chain.setAttribute("aria-label","Handover responsibility and live stage");
    for(const stage of stages){const item=document.createElement("div");item.className="kc-chain-stage "+stage.state;item.setAttribute("role","listitem");if(stage.state==="current")item.setAttribute("aria-current","step");const title=document.createElement("b"),name=document.createElement("span"),detail=document.createElement("span"),state=document.createElement("small");title.textContent=stage.title;name.textContent=stage.name;detail.textContent=stage.detail;state.textContent=stage.state==="done"?"Complete":stage.state==="current"?"Current step":"Waiting";item.append(title,name,detail,state);chain.append(item)}
    root.append(chain);
  }
  function owner(){
    if(typeof pageName==="undefined"||pageName!=="detail"||typeof current==="undefined"||!current)return;
    const root=document.getElementById("canvas"),tabs=root&&root.querySelector(".tabs");if(!tabs||root.querySelector(".kc-guide"))return;
    const h=current.handover,n=current.sources.length,open=current.questions.filter(q=>q.status==="Open").length,missing=current.fields.filter(f=>f.state==="Missing").length,waiting=current.fields.filter(f=>!f.approved&&f.state!=="Missing").length;
    let label="Review fields",copy="Compare each draft with its cited source. Edit unclear claims, choose recipient visibility, then approve supported fields.",target="content";
    if(!n){label="Add project sources";copy="Attach a README, notes, issue export, tests, or chat before reviewing claims.";target="sources";}
    else if(open){label="Resolve reviewer questions";copy=open+" question(s) are open. Ask the builder while the context is fresh.";target="questions";}
    else if(waiting){label="Review "+waiting+" draft field(s)";copy="Check citations, edit unsupported text, choose who can see each field, then approve.";target="content";}
    else if(h.status!=="Published"){label="Review fields";copy="Preview what the engineer will see. Publish only after every visible field is approved.";target="content";}
    else{label="View the shared version";copy="This handover is published. Inspect the engineer view and acknowledgement.";target="content";}
    const canPublish=["Submitted","In review"].includes(h.status)&&current.fields.some(f=>f.visible_to_recipient)&&current.fields.filter(f=>f.visible_to_recipient&&!f.approved).length===0;
    const base=guideBase("Next step: "+label,copy),next=document.createElement("button");next.type="button";next.className="kc-guide-next";next.textContent=label+" ->";next.onclick=()=>{if(canPublish&&!open){publish();return;}tab=target;render();};base.h.append(next);
    responsibilityChain(base.g,h);
    const steps=document.createElement("div");steps.className="kc-guide-steps";
    step(steps,"1. Gather evidence",n+" resource(s) attached.",n?"done":"current","Review resources",()=>{tab="sources";render();});
    step(steps,"2. Resolve gaps",open+" open / "+missing+" missing fields.",open?"current":missing?"":"done","View questions",()=>{tab="questions";render();});
    step(steps,"3. Review and approve",waiting+" supported field(s) need approval.",waiting?"current":current.fields.some(f=>f.approved)?"done":"","Review fields",()=>{tab="content";render();});
    step(steps,"4. Share safely",h.status==="Published"?"Published to the assigned engineer.":"Only approved fields marked for sharing appear.",h.status==="Published"?"done":"","Recipient preview",()=>recipientView());
    base.g.append(steps);mount(root,tabs,base.g);
  }
  function builder(){
    if(typeof current==="undefined"||!current)return;const root=document.getElementById("main"),tabs=root&&root.querySelector(".tabs");if(!tabs||root.querySelector(".kc-guide"))return;
    const h=current.handover,n=current.sources.length,open=current.questions.filter(q=>q.status==="Open").length,drafted=current.fields.some(f=>f.state!=="Missing"&&String(f.value||"").trim()),submitted=["Submitted","Published"].includes(h.status);
    let label="Add a project resource",copy="Start with files and notes you already have: README, code, chat, issues, tests, or setup steps.",target="resources";
    if(n&&!drafted){label="Draft fields from sources";copy="The sources are ready. Generate cited fields, then check every answer.";target="fields";}
    else if(open){label="Answer "+open+" owner question(s)";copy="Answer while the details are fresh. If you do not know, say so; do not guess.";target="questions";}
    else if(n&&!submitted){label="Submit to senior reviewer";copy="Check your draft and sources, then submit. The senior reviewer approves and controls sharing.";target="submit";}
    else if(submitted){label="Review submitted draft";copy="Your handover is with the reviewer. Return to update details or answer follow-up questions.";target="fields";}
    const base=guideBase("Your handover, step by step",copy),next=document.createElement("button");next.type="button";next.className="kc-guide-next";next.textContent=label+" →";next.onclick=()=>{if(target==="submit"){submitHandover();return;}if(target==="fields"&&n&&!drafted){extract();return;}tab=target;workspace();};base.h.append(next);
    responsibilityChain(base.g,h);
    const steps=document.createElement("div");steps.className="kc-guide-steps";
    step(steps,"1. Add evidence",n+" project resource(s).",n?"done":"current","Review resources",()=>{tab="resources";workspace();});
    step(steps,"2. Draft and check",drafted?"Review and correct the drafted details.":"Generate cited answers from sources.",drafted?"done":n?"current":"","Template fields",()=>{tab="fields";workspace();});
    step(steps,"3. Resolve gaps",open?open+" owner question(s) need answers.":"No open owner questions.",open?"current":drafted?"done":"","Open questions",()=>{tab="questions";workspace();});
    step(steps,"4. Submit for review",submitted?"Submitted to the senior reviewer.":"The owner approves and chooses what to share.",submitted?"done":"","Submit draft",()=>submitHandover());
    base.g.append(steps);mount(root,tabs,base.g);
  }
  function recipient(){
    if(typeof current==="undefined"||!current)return;const root=document.getElementById("main"),tabs=root&&root.querySelector(".tabs");if(!tabs||root.querySelector(".kc-guide"))return;
    const base=guideBase("Pick up the work confidently","Read the next-build plan, inspect sources for claims you rely on, then ask about anything unclear. Acknowledgement records receipt of this version.");
    responsibilityChain(base.g,current.handover);
    const steps=document.createElement("div");steps.className="kc-guide-steps";
    step(steps,"1. Read the handover","Review current state, decisions, gaps, and next tasks.","done");
    step(steps,"2. Verify from sources","Use citations and the timeline to inspect approved evidence.","","View timeline",()=>{tab="timeline";workspace();});
    step(steps,"3. Ask and acknowledge","Use sourced Q&A; acknowledge after reviewing this version.","","Ask a question",()=>{tab="qa";workspace();});
    base.g.append(steps);mount(root,tabs,base.g);
  }
  const run=()=>{try{if(location.pathname==="/app")owner();else if(location.pathname==="/employee")builder();else if(location.pathname==="/recipient")recipient();}catch(e){console.warn("Journey guide did not render",e);}};
  const root=document.getElementById(location.pathname==="/employee"||location.pathname==="/recipient"?"main":"canvas");
  if(root)new MutationObserver(()=>requestAnimationFrame(run)).observe(root,{childList:true,subtree:true});
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",run,{once:true});else run();
})();
