// Delivery health board prototype. Everything is local to the page: nothing is stored or sent.
// Sample data throughout. The only real facts are the ones marked "OpenAI public page", which link to their source.
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var DEP = 'https://developers.openai.com/api/docs/deprecations';
  var WA = 'https://help.openai.com/en/articles/10875114-workspace-analytics-for-chatgpt-enterprise-and-edu';
  var SURV = 'https://help.openai.com/en/articles/20001149-managing-impact-surveys-in-admin-console';
  var QS = 'https://help.openai.com/en/articles/20001264-chatgpt-enterprise-admin-quickstart';
  var RT = 'https://developers.openai.com/api/docs/guides/reserved-tier';
  var UI = 'https://learn.chatgpt.com/docs/enterprise/usage-insights';
  var TP = 'https://trust.openai.com/';
  var PRES = 'https://help.openai.com/en/articles/20001405-openai-presence';

  var LABEL = { ok: 'Passed', gate: 'At risk', none: 'Late', wait: 'Not due', dash: 'No data' };
  var RLABEL = { open: 'Open', high: 'Open, high', closed: 'Closed', acc: 'Accepted' };
  var RCLASS = { open: 'gate', high: 'none', closed: 'ok', acc: 'wait' };
  var SRC = { stated: 'Stated in a system', joined: 'Joined from two systems', derived: 'Derived', entered: 'Entered by a person', pub: 'OpenAI public page' };

  // s = status at each review. why / ev may be one value for all reviews or one per review.
  var GATES = [
    { id: 'g1', n: 1, name: 'Scope and measures signed', owner: 'Chief Claims Officer', team: 'Customer', due: 2, s: { w6: 'ok', w10: 'ok', w14: 'ok' },
      why: 'The sponsor signed the scope note in week 2. It names the outcome, the measure and who reports it.',
      ev: [{ t: 'Signed scope note, dated week 2.', k: 'entered' }, { t: 'OpenAI’s published sequence for managed deployments starts with outcomes and success criteria.', k: 'pub', u: PRES }],
      waits: 'Nothing. It is first.', change: 'A new sponsor, or a second use case added.' },
    { id: 'g2', n: 2, name: 'Baseline set', owner: 'Claims operations lead', team: 'Customer', due: 2, s: { w6: 'ok', w10: 'ok', w14: 'ok' },
      why: 'Both halves of the baseline exist: a figure from the claims system and a first survey of the pilot group.',
      ev: [{ t: 'Time from first notice to first contact, read from the claims system’s own report.', k: 'stated' }, { t: 'Baseline survey started by the workspace admin in week 1.', k: 'entered' }, { t: 'OpenAI’s scheduled impact surveys run at day 120 and day 240, so a week-one baseline has to be started by the admin.', k: 'pub', u: SURV }],
      waits: 'Gate 1, and access to the claims reports.', change: 'A change to the measure after week 2 resets it.' },
    { id: 'g3', n: 3, name: 'Security, privacy and legal review', owner: 'Security reviewer', team: 'Customer', due: 8, s: { w6: 'gate', w10: 'ok', w14: 'ok' },
      why: { w6: 'The reviewer has OpenAI’s public documents. The partner’s data-flow diagram is still a draft, and the review cannot close without it.', w10: 'Closed in week 8 with two conditions, both met.', w14: 'Closed in week 8 with two conditions, both met.' },
      ev: { w6: [{ t: 'Reviewer’s checklist, part answered. The open items all wait on the diagram.', k: 'entered' }, { t: 'OpenAI’s Trust Portal lists its compliance documents. The SOC 2 report is by request.', k: 'pub', u: TP }],
            w10: [{ t: 'Reviewer’s sign-off, week 8.', k: 'entered' }, { t: 'Final data-flow diagram from the partner.', k: 'stated' }] },
      waits: 'The partner’s data-flow diagram.', change: 'A new data source, or a new region for the data.' },
    { id: 'g4', n: 4, name: 'Identity ready', owner: 'Identity admin', team: 'Customer', due: 6, s: { w6: 'ok', w10: 'ok', w14: 'ok' },
      why: 'The domain is verified, single sign-on was tested by a pilot member, and directory sync is running.',
      ev: [{ t: 'Sign-in test by a pilot member, week 5.', k: 'entered' }, { t: 'Directory sync log shows the pilot group.', k: 'stated' }, { t: 'OpenAI’s quickstart puts sign-on and directory sync before broad invitations.', k: 'pub', u: QS }],
      waits: 'Nothing outside the customer.', change: 'A change of identity provider.' },
    { id: 'g5', n: 5, name: 'Evals at the agreed mark', owner: 'Forward Deployed Engineering lead', team: 'OpenAI', due: 8, s: { w6: 'wait', w10: 'ok', w14: 'ok' },
      why: { w6: 'Not due until week 8. The pass mark was agreed in week 2. The first full run is next week.', w10: 'The latest run is above the agreed mark on the example claims the adjusters chose.', w14: 'Passed in week 8. Re-run after launch on live claims, still above the mark.' },
      ev: { w6: [{ t: 'Pass mark agreed with adjusters in week 2.', k: 'entered' }], w10: [{ t: 'Pass mark agreed with adjusters in week 2.', k: 'entered' }, { t: 'Latest eval run on the example claims.', k: 'derived' }] },
      waits: 'Example claims from the customer, and the test environment.', change: 'A model change. Any change of model means the evals run again.' },
    { id: 'g6', n: 6, name: 'Integration accepted', owner: 'Partner engagement lead', team: 'Partner', due: 9, s: { w6: 'wait', w10: 'gate', w14: 'ok' },
      why: { w6: 'Not due until week 9.', w10: 'Reading from the claims system works. Two write actions still fail in the test environment, and the next change window is in week 11.', w14: 'Accepted in week 11, two weeks late. Launch went ahead with the two write actions switched off, by the sponsor’s decision.' },
      ev: { w6: [], w10: [{ t: 'Partner’s test report, week 10.', k: 'stated' }, { t: 'Change calendar from the claims platform owner.', k: 'stated' }], w14: [{ t: 'Acceptance note signed by the claims platform owner, week 11.', k: 'entered' }, { t: 'Sponsor’s decision recorded at the week 10 review.', k: 'entered' }] },
      waits: 'The claims system’s change window.', change: 'An earlier change window, or a launch without the write actions.' },
    { id: 'g7', n: 7, name: 'Model and capacity confirmed', owner: 'Account director', team: 'OpenAI', due: 9, s: { w6: 'dash', w10: 'ok', w14: 'ok' },
      why: { w6: 'There is no load estimate yet, so there is nothing to judge. That is a dash, not a green light.', w10: 'The model’s published shutdown date falls after the adoption review. Capacity was sized from acceptance testing and ordered.', w14: 'Confirmed in week 9. Peak usage since launch has stayed inside the order.' },
      ev: { w6: [], w10: [{ t: 'Shutdown date read from OpenAI’s deprecations page and recorded beside the launch date.', k: 'pub', u: DEP }, { t: 'Peak load estimated from acceptance testing.', k: 'derived' }, { t: 'Capacity order confirmed by the account director.', k: 'entered' }, { t: 'Reserved capacity is bought per model, through sales.', k: 'pub', u: RT }] },
      waits: 'A load estimate from acceptance testing.', change: 'A retirement notice for the chosen model, or a larger pilot group.' },
    { id: 'g8', n: 8, name: 'Training and support path', owner: 'Change lead', team: 'Customer', due: 10, s: { w6: 'wait', w10: 'dash', w14: 'ok' },
      why: { w6: 'Not due until week 10. Sessions are not scheduled yet.', w10: 'Sessions were scheduled, but nobody has reported attendance. Scheduled is not attended.', w14: 'The pilot group attended before launch, and the support path was used in the first week.' },
      ev: { w6: [], w10: [], w14: [{ t: 'Attendance reported by the change lead.', k: 'entered' }, { t: 'Support tickets from the pilot’s first week.', k: 'stated' }] },
      waits: 'The pilot group named, and a go decision for the wider rollout.', change: 'A new pilot group.', ask: true },
    { id: 'g9', n: 9, name: 'First adoption review held', owner: 'Delivery Lead', team: 'OpenAI', due: 14, after: true, s: { w6: 'wait', w10: 'wait', w14: 'ok' },
      why: { w6: 'Not due until week 14.', w10: 'Not due until week 14.', w14: 'Held in week 14, with numbers from three sources and their dates.' },
      ev: { w6: [], w10: [], w14: [{ t: 'Review notes and decisions, week 14.', k: 'entered' }] },
      waits: 'Launch, and three weeks of use.', change: 'A launch slip moves it by the same number of weeks.' }
  ];

  var STREAMS = [
    ['Outcome and measures', 'Customer', 'Chief Claims Officer', 'g1'], ['Baseline', 'Customer', 'Claims operations lead', 'g2'],
    ['Security, privacy and legal review', 'Customer', 'Security reviewer', 'g3'], ['Identity and access', 'Customer', 'Identity admin', 'g4'],
    ['Claims system access', 'Customer', 'Claims platform owner', 'g6'], ['Training and floor support', 'Customer', 'Change lead', 'g8'],
    ['The integrated plan and reviews', 'OpenAI', 'Delivery Lead', 'g1'], ['Agent build and evals', 'OpenAI', 'Forward Deployed Engineering lead', 'g5'],
    ['Model and capacity', 'OpenAI', 'Account director', 'g7'], ['Workspace guidance', 'OpenAI', 'AI advisor', 'g4'],
    ['Measurement', 'OpenAI', 'Delivery Lead', 'g9'], ['Support path at launch', 'OpenAI', 'Support lead', 'g8'],
    ['Integration with the claims system', 'Partner', 'Partner engagement lead', 'g6'], ['Data-flow diagram and security answers', 'Partner', 'Partner architect', 'g3'],
    ['Acceptance testing with adjusters', 'Partner', 'Partner test lead', 'g6'], ['Rollout and training delivery', 'Partner', 'Partner change manager', 'g8'],
    ['Handover', 'Partner', 'Partner engagement lead', 'g9']
  ].map(function (a, i) { return { id: 's' + i, name: a[0], team: a[1], owner: a[2], gate: a[3] }; });

  var RISKS = [
    { id: 'r1', name: 'The claims system’s change window falls after the integration date', owner: 'Claims platform owner', gate: 'g6', s: { w6: 'open', w10: 'high', w14: 'closed' },
      why: { w6: 'The partner needs two write actions approved. The next change window is week 11, the launch week.', w10: 'The window has not moved. Decision needed today: launch with the two write actions switched off, or move the launch.', w14: 'The sponsor chose to launch with the write actions off. They were switched on in week 12.' },
      ev: [{ t: 'Change calendar from the claims platform owner.', k: 'stated' }] },
    { id: 'r2', name: 'Training is scheduled but attendance is not reported', owner: 'Change lead', gate: 'g8', s: { w6: 'open', w10: 'open', w14: 'closed' },
      why: { w6: 'Sessions are not scheduled yet.', w10: 'A full calendar is not a trained pilot group. The gate stays blank until someone reports who came.', w14: 'Attendance was reported before launch.' },
      ev: [] },
    { id: 'r3', name: 'The model retires close to launch', owner: 'Account director', gate: 'g7', s: { w6: 'open', w10: 'closed', w14: 'closed' },
      why: { w6: 'The plan has to name the model’s shutdown date before the launch date is fixed. OpenAI publishes the date, and gives generally available models at least six months’ notice.', w10: 'Checked in week 9. The date is recorded on gate 7.', w14: 'Checked in week 9. The date is recorded on gate 7.' },
      ev: [{ t: 'Notice periods and shutdown dates on OpenAI’s deprecations page.', k: 'pub', u: DEP }] },
    { id: 'r4', name: 'Capacity is ordered before the load is known', owner: 'Account director', gate: 'g7', s: { w6: 'open', w10: 'closed', w14: 'closed' },
      why: { w6: 'An order placed now would be a guess. It waits for acceptance testing.', w10: 'Sized from acceptance testing, then ordered.', w14: 'Sized from acceptance testing, then ordered.' },
      ev: [{ t: 'Reserved capacity is bought per model, through sales.', k: 'pub', u: RT }] },
    { id: 'r5', name: 'Adoption figures are up to two days old on review day', owner: 'Delivery Lead', gate: 'g9', s: { w6: 'acc', w10: 'acc', w14: 'acc' },
      why: 'OpenAI says workspace analytics is refreshed every 1 to 24 hours, with a target of up to 48 hours. This cannot be fixed, so it is accepted, and every adoption figure shows its as-of date.',
      ev: [{ t: 'Data freshness, in OpenAI’s workspace analytics article.', k: 'pub', u: WA }] },
    { id: 'r6', name: 'No baseline survey unless the admin starts one', owner: 'Claims operations lead', gate: 'g2', s: { w6: 'closed', w10: 'closed', w14: 'closed' },
      why: 'OpenAI’s scheduled surveys run at day 120 and day 240. The workspace admin started one in week 1 instead.',
      ev: [{ t: 'Survey timing, in OpenAI’s impact surveys article.', k: 'pub', u: SURV }] }
  ];

  var ADOPT = [
    { id: 'a1', name: 'Pilot adjusters using it each week', base: 'New', now: '68%', k: 'stated', from: 'Analytics API',
      why: 'Read from the workspace’s analytics API. It is a count of people, so it says who used it, not what they finished.', ev: [{ t: 'Workspace analytics can lag by up to 48 hours.', k: 'pub', u: WA }] },
    { id: 'a2', name: 'Time from first notice to first contact', base: '9.5 hours', now: '7.1 hours', k: 'stated', from: 'Customer’s claims system',
      why: 'The outcome the sponsor chose. Both figures come from the same report in the customer’s claims system, three weeks apart. Three weeks is short, and the review says so.', ev: [] },
    { id: 'a3', name: 'Drafts accepted without edits', base: 'New', now: '54%', k: 'joined', from: 'Agent logs joined to the claims system',
      why: 'Joined by claim number. Claims that could not be matched are left out and counted separately, not guessed.', ev: [] },
    { id: 'a4', name: 'Hours saved per adjuster each week', base: 'New', now: '3, an estimate', k: 'entered', from: 'Impact survey, self-reported',
      why: 'People’s own estimate from the survey. It is shown as an estimate and never added to the measured figures.', ev: [{ t: 'OpenAI’s guide says to keep estimates labeled as estimates.', k: 'pub', u: UI }] },
    { id: 'a5', name: 'Credits used this week', base: 'New', now: '41,000', k: 'stated', from: 'Usage export',
      why: 'Read from the usage export. Credits show consumption, not finished work, so this figure never stands alone.', ev: [{ t: 'OpenAI’s guide: activity counts do not measure completed work.', k: 'pub', u: UI }] }
  ];

  var state = { rev: 'w10', team: 'all', slip: 0, sel: null, entered: false };

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function at(v) { return v && typeof v === 'object' && !Array.isArray(v) ? (v[state.rev] !== undefined ? v[state.rev] : v.w10) : v; }
  function gate(id) { return GATES.filter(function (g) { return g.id === id; })[0]; }
  function gstat(g) { return (g.id === 'g8' && state.rev === 'w10' && state.entered) ? 'ok' : g.s[state.rev]; }
  function mark(k, label) { return '<span class="st ' + k + '">' + esc(label) + '</span>'; }
  function tag(k) { return '<span class="tagsrc' + (k === 'pub' ? ' pub' : '') + '">' + SRC[k] + '</span>'; }
  function pressed(kind, id) { return state.sel && state.sel.kind === kind && state.sel.id === id ? 'true' : 'false'; }
  function plural(n, w) { return n + ' ' + w + (n === 1 ? '' : 's'); }

  function confidence() {
    var c = { ok: 0, gate: 0, none: 0, wait: 0, dash: 0 };
    GATES.forEach(function (g) { if (!g.after) c[gstat(g)]++; });
    if (state.rev === 'w14') return { big: 'Live', k: 'ok', text: 'Launched in week 11. Seven launch gates passed on time and one passed two weeks late. The late one is integration.', c: c };
    if (c.dash) return { big: '—', k: 'dash', c: c, text: 'No launch confidence is stated. ' + plural(c.dash, 'gate') + (c.dash === 1 ? ' has' : ' have') + ' no data' + (c.wait ? ', and ' + c.wait + (c.wait === 1 ? ' is' : ' are') + ' not due yet' : '') + '. I will not put a word over a blank.' };
    if (c.none) return { big: 'Low', k: 'none', c: c, text: plural(c.none, 'gate') + ' late. ' + c.ok + ' of 8 have passed.' };
    if (c.gate) return { big: 'Medium', k: 'gate', c: c, text: c.ok + ' of 8 launch gates have passed with evidence. ' + plural(c.gate, 'gate') + (c.gate === 1 ? ' is' : ' are') + ' at risk: integration. The decision on it is on today’s list.' };
    if (c.wait) return { big: '—', k: 'dash', c: c, text: 'Too early to say. ' + plural(c.wait, 'gate') + ' not due yet.' };
    return { big: 'High', k: 'ok', c: c, text: 'All 8 launch gates have passed with evidence.' };
  }

  function renderConf() {
    var f = confidence();
    $('conf').innerHTML = '<div class="big ' + f.k + '">' + f.big + '</div><div><b style="display:block;margin-bottom:4px">' + (state.rev === 'w14' ? 'Launch' : 'Launch confidence') + '</b><p>' + esc(f.text) + '</p>'
      + '<button class="btn sm ghost" type="button" data-kind="conf" data-id="c" style="margin-top:10px">See what it rests on</button></div>'
      + '<p class="rule">The rule: launch confidence is derived from the eight launch gates. Any gate with no data, and no confidence is stated. Any gate late, Low. Any at risk, Medium. Otherwise High.</p>';
    $('gcount').textContent = 'Launch gates: ' + f.c.ok + ' passed, ' + f.c.gate + ' at risk, ' + f.c.none + ' late, ' + f.c.wait + ' not due, ' + f.c.dash + ' no data';
  }

  function renderGates() {
    $('gates').innerHTML = GATES.map(function (g) {
      var k = gstat(g);
      return '<button class="pick" type="button" data-kind="gate" data-id="' + g.id + '" aria-pressed="' + pressed('gate', g.id) + '">' + mark(k, LABEL[k])
        + '<b>' + g.n + '. ' + esc(g.name) + '</b><small>' + esc(g.owner) + ', ' + g.team + '. Due week ' + g.due + '.</small></button>';
    }).join('');
  }

  function renderStreams() {
    $('streams').innerHTML = STREAMS.filter(function (s) { return state.team === 'all' || s.team === state.team; }).map(function (s) {
      var k = gstat(gate(s.gate));
      return '<button class="pick" type="button" data-kind="stream" data-id="' + s.id + '" aria-pressed="' + pressed('stream', s.id) + '"><b>' + esc(s.name) + '</b>' + mark(k, LABEL[k])
        + '<small>' + s.team + ' &middot; ' + esc(s.owner) + ' &middot; gate ' + gate(s.gate).n + '</small></button>';
    }).join('');
  }

  function renderRisks() {
    var order = { high: 0, open: 1, acc: 2, closed: 3 };
    $('risks').innerHTML = RISKS.slice().sort(function (a, b) { return order[a.s[state.rev]] - order[b.s[state.rev]]; }).map(function (r) {
      var k = r.s[state.rev];
      return '<button class="pick" type="button" data-kind="risk" data-id="' + r.id + '" aria-pressed="' + pressed('risk', r.id) + '"><b>' + esc(r.name) + '</b>' + mark(RCLASS[k], RLABEL[k])
        + '<small>' + esc(r.owner) + ' &middot; threatens gate ' + gate(r.gate).n + '</small></button>';
    }).join('');
  }

  function renderAdopt() {
    var live = state.rev === 'w14';
    $('adopt').innerHTML = ADOPT.map(function (a) {
      return '<tr><td><button type="button" data-kind="adopt" data-id="' + a.id + '">' + esc(a.name) + '</button></td><td class="num">' + (a.base === 'New' ? '<span class="note" style="font-family:IT;font-size:14px">None. New tool.</span>' : esc(a.base)) + '</td>'
        + '<td class="num">' + (live ? esc(a.now) : '<span class="st dash">No data</span>') + '</td><td>' + (live ? tag(a.k) + ' <span class="note">' + esc(a.from) + '</span>' : '<span class="note">Nothing to show before launch</span>') + '</td></tr>';
    }).join('');
    $('asof').textContent = live ? 'Figures as of two days before the review.' : 'Launch is week 11. Nothing is live yet.';
    $('adoptNote').textContent = live ? 'Three weeks of use. Enough to see direction, not enough to claim a result. Every figure here is a sample value.' : 'Before launch this table is empty on purpose. A baseline is a number. A blank is a dash.';
  }

  function renderRamp() {
    var base = [8, 22, 38, 55, 70, 82, 90, 95], h = [];
    for (var i = 0; i < 8; i++) h.push(i - state.slip >= 0 ? base[i - state.slip] : 0);
    $('bars').innerHTML = h.map(function (v) { return '<div class="' + (v ? '' : 'z') + '" style="height:' + (v || 2) + '%"></div>'; }).join('');
    $('barl').innerHTML = h.map(function (v, i) { return '<span>wk ' + (11 + i) + '</span>'; }).join('');
    $('rampText').textContent = state.slip
      ? 'Two weeks late, the same ramp starts in week 13. In week 18 the pilot is where it would have been in week 16. The account team’s forecast and the capacity start date should both move by two weeks. I would say that at the review where the slip is decided, not at quarter end.'
      : 'On plan, usage starts in week 11 and reaches its pilot level around week 16. The capacity order starts the same week.';
  }

  function evList(ev) {
    return ev && ev.length ? '<ul>' + ev.map(function (e) { return '<li>' + tag(e.k) + '<br>' + esc(e.t) + (e.u ? ' <a href="' + e.u + '">source</a>' : '') + '</li>'; }).join('') + '</ul>'
      : '<p>None yet. With no evidence the status is a dash.</p>';
  }
  var LEGEND = '<div class="legend"><b style="color:var(--soft)">How to read a source tag</b><br>' + tag('stated') + tag('joined') + tag('derived') + tag('entered') + tag('pub')
    + '<br>The first four are sample data. The last is a real fact, with a link.</div>';

  function gateBody(g, lead) {
    var k = gstat(g), entered = g.id === 'g8' && state.rev === 'w10' && state.entered;
    var why = entered ? 'The change lead reports at this review that the pilot group has attended. That is a person’s word, and it is marked that way.' : at(g.why);
    var ev = entered ? [{ t: 'Attendance for the pilot group, reported by the change lead at this review.', k: 'entered' }] : at(g.ev);
    return (lead || '') + '<h3>' + g.n + '. ' + esc(g.name) + '</h3>' + mark(k, LABEL[k])
      + '<div class="meta"><span>Owner</span><b>' + esc(g.owner) + ', ' + g.team + '</b><span>Due</span><b>Week ' + g.due + '</b></div>'
      + '<h4>Why it has this status</h4><p>' + esc(why) + '</p><h4>Evidence</h4>' + evList(ev)
      + '<h4>Waits on</h4><p>' + esc(g.waits) + '</p><h4>What would change it</h4><p>' + esc(g.change) + '</p>'
      + (g.ask && state.rev === 'w10' && !state.entered ? '<button class="btn sm" type="button" id="enter">Record what the change lead reports</button><p class="note" style="margin-top:8px">A sample action. It shows the confidence figure moving only when a person supplies evidence.</p>' : '');
  }

  function renderWhy() {
    var s = state.sel, h;
    if (!s) h = '<h3>Why this status</h3><p>Select a gate, a risk, a workstream or a number. This panel shows the reason, the evidence and where each piece came from.</p>';
    else if (s.kind === 'gate') h = gateBody(gate(s.id));
    else if (s.kind === 'stream') {
      var st = STREAMS.filter(function (x) { return x.id === s.id; })[0];
      h = gateBody(gate(st.gate), '<p class="note">Workstream</p><h3 style="margin-bottom:6px">' + esc(st.name) + '</h3><p>' + st.team + ' &middot; ' + esc(st.owner) + '. Its status is its gate’s status:</p><div style="height:14px"></div>');
    } else if (s.kind === 'risk') {
      var r = RISKS.filter(function (x) { return x.id === s.id; })[0], k = r.s[state.rev], g = gate(r.gate);
      h = '<p class="note">Risk</p><h3>' + esc(r.name) + '</h3>' + mark(RCLASS[k], RLABEL[k])
        + '<div class="meta"><span>Owner</span><b>' + esc(r.owner) + '</b><span>Threatens</span><b>Gate ' + g.n + ', ' + esc(g.name.toLowerCase()) + '</b></div>'
        + '<h4>Why it has this status</h4><p>' + esc(at(r.why)) + '</p><h4>Evidence</h4>' + evList(r.ev)
        + '<button class="btn sm ghost" type="button" data-kind="gate" data-id="' + g.id + '">Open gate ' + g.n + '</button>';
    } else if (s.kind === 'adopt') {
      var a = ADOPT.filter(function (x) { return x.id === s.id; })[0], live = state.rev === 'w14';
      h = '<p class="note">Measure</p><h3>' + esc(a.name) + '</h3>' + (live ? tag(a.k) : mark('dash', 'No data'))
        + '<div class="meta"><span>Baseline</span><b>' + (a.base === 'New' ? 'None. The tool is new.' : esc(a.base) + ', week 1') + '</b><span>Now</span><b>' + (live ? esc(a.now) : 'Not live yet') + '</b><span>From</span><b>' + esc(a.from) + '</b></div>'
        + '<h4>How to read it</h4><p>' + esc(a.why) + '</p>' + (a.ev.length ? '<h4>Why it is shown this way</h4>' + evList(a.ev) : '') + '<p class="note" style="margin-top:12px">The values are samples.</p>';
    } else {
      h = '<h3>What launch confidence rests on</h3><p>' + esc(confidence().text) + '</p><ul>' + GATES.filter(function (g) { return !g.after; }).map(function (g) {
        var k = gstat(g); return '<li>' + mark(k, LABEL[k]) + '<br>' + g.n + '. ' + esc(g.name) + '</li>';
      }).join('') + '</ul>';
    }
    $('why').innerHTML = h + LEGEND;
  }

  function seg(id, attr, val) { $(id).querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute(attr)) === String(val)); }); }
  function render() { renderConf(); renderGates(); renderStreams(); renderRisks(); renderAdopt(); renderRamp(); renderWhy(); }

  document.addEventListener('click', function (e) {
    var t = e.target.closest('button'); if (!t || !t.closest('#proto')) return;
    if (t.hasAttribute('data-rev')) { state.rev = t.getAttribute('data-rev'); seg('reviews', 'data-rev', state.rev); return render(); }
    if (t.hasAttribute('data-team')) { state.team = t.getAttribute('data-team'); seg('teams', 'data-team', state.team); return renderStreams(); }
    if (t.hasAttribute('data-slip')) { state.slip = +t.getAttribute('data-slip'); seg('slip', 'data-slip', state.slip); return renderRamp(); }
    if (t.id === 'enter') { state.entered = true; return render(); }
    if (t.hasAttribute('data-kind')) {
      state.sel = { kind: t.getAttribute('data-kind'), id: t.getAttribute('data-id') }; render();
      // On a phone the panel sits below the board, so bring it into view.
      if (window.matchMedia && window.matchMedia('(max-width:900px)').matches) $('why').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });

  state.sel = { kind: 'gate', id: 'g8' };
  render();
})();
