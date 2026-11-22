# Builds the five pages of the OpenAI pitch site into this folder.
# Run: python build.py
import html, os
HERE = os.path.dirname(os.path.abspath(__file__))
E = html.escape
READ = 'November 22, 2026'

NAV = [('index.html', 'The plan'), ('evidence.html', 'The evidence'), ('prototype.html', 'The prototype'), ('how.html', 'How I built it'), ('why.html', 'Why me')]

def page(fn, title, desc, body, script=''):
    nav = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == fn else '', t) for h, t in NAV)
    out = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           '<meta name="robots" content="noindex,nofollow"><title>%s</title><meta name="description" content="%s">'
           '<link rel="stylesheet" href="assets/site.css"></head><body><a class="skip" href="#main">Skip to content</a>'
           '<div class="flag"><div class="w"><b>Unofficial.</b> A job application for OpenAI&rsquo;s Applied AI Delivery Lead role, built from public pages. Not affiliated with OpenAI.</div></div>'
           '<header class="w nav"><a class="me" href="index.html"><i></i>Richard J. Valeo</a><nav aria-label="Pages">%s</nav></header>'
           '<main id="main">%s</main>'
           '<footer class="w foot"><span>Richard J. Valeo &middot; Georgetown, Colorado &middot; <a href="https://rjvaleo.github.io/">rjvaleo.github.io</a> &middot; <a href="https://www.linkedin.com/in/rjvaleo">LinkedIn</a></span>'
           '<span>Public pages read on %s. Nothing here comes from inside OpenAI.</span></footer>%s</body></html>') % (E(title), E(desc), nav, body, READ, script)
    open(os.path.join(HERE, fn), 'w', encoding='utf-8', newline='\n').write(out)
    print('wrote', fn, len(out))

def a(url, text): return '<a href="%s">%s</a>' % (url, text)

# public OpenAI pages cited more than once
U_ROLLOUT = 'https://learn.chatgpt.com/docs/enterprise/admin-setup'
U_QUICK = 'https://help.openai.com/en/articles/20001264-chatgpt-enterprise-admin-quickstart'
U_PRES = 'https://help.openai.com/en/articles/20001405-openai-presence'
U_DEP = 'https://developers.openai.com/api/docs/deprecations'
U_SURV = 'https://help.openai.com/en/articles/20001149-managing-impact-surveys-in-admin-console'
U_WA = 'https://help.openai.com/en/articles/10875114-workspace-analytics-for-chatgpt-enterprise-and-edu'
U_UI = 'https://learn.chatgpt.com/docs/enterprise/usage-insights'
U_GOV = 'https://learn.chatgpt.com/docs/enterprise/governance'
U_FDE = 'https://openai.com/index/forward-deployed-engineering-means/'
U_PN = 'https://openai.com/business/partners/'
U_RT = 'https://developers.openai.com/api/docs/guides/reserved-tier'
U_ST = 'https://openai.com/api-scale-tier/'
U_STATUS = 'https://status.openai.com/'
U_TRUST = 'https://trust.openai.com/'

# ---------------------------------------------------------------- the plan
# (workstream, owner role, what it delivers, waits-on kind, what it waits on, week)
# waits-on kind: 'ok' waits on nobody outside its own team, 'gate' waits on another team
BOARD = [
 ('Customer', 'Fernhill Mutual, a made-up insurer.', [
   ('Outcome and measures', 'Chief Claims Officer', 'The result to improve, the measure, and a signature.', 'ok', 'Nothing. It is first.', 2),
   ('Baseline', 'Claims operations lead', 'The starting figure, from the claims system and a first survey.', 'ok', 'Its own claims reports.', 2),
   ('Security, privacy and legal review', 'Security reviewer', 'A sign-off, with any conditions written down.', 'gate', 'The partner&rsquo;s data-flow diagram, and OpenAI&rsquo;s Trust Portal documents.', 8),
   ('Identity and access', 'Identity admin', 'Verified domain, single sign-on and directory sync.', 'ok', 'Nothing outside the customer.', 6),
   ('Claims system access', 'Claims platform owner', 'A test environment and a change window.', 'gate', 'The partner&rsquo;s list of actions to approve.', 9),
   ('Training and floor support', 'Change lead', 'A trained pilot group, and someone to call.', 'gate', 'Training material from the partner.', 10)]),
 ('OpenAI', 'Role names as they appear on OpenAI&rsquo;s public pages.', [
   ('The integrated plan and reviews', 'Delivery Lead', 'One plan, one board, and a review every two weeks.', 'gate', 'A named owner for every other workstream.', 1),
   ('Agent build and evals', 'Forward Deployed Engineering lead', 'The agent, and evals with a pass mark agreed first.', 'gate', 'Example claims and a test environment from the customer.', 8),
   ('Model and capacity', 'Account director', 'A model with its retirement date checked, and capacity ordered.', 'gate', 'A load estimate from the partner&rsquo;s acceptance testing.', 9),
   ('Workspace guidance', 'AI advisor', 'Setup advice for the claims organization&rsquo;s workspace.', 'gate', 'The customer&rsquo;s identity work.', 6),
   ('Measurement', 'Delivery Lead', 'Adoption against the baseline, with a source on every number.', 'gate', 'The baseline, and analytics access from the customer&rsquo;s admin.', 14),
   ('Support path at launch', 'Support lead', 'A named route for the first weeks.', 'gate', 'Named admins and an escalation contact from the customer.', 10)]),
 ('Partner', 'A delivery partner from the Partner Network.', [
   ('Integration with the claims system', 'Partner engagement lead', 'The agent reading from and writing to the claims system.', 'gate', 'API access from OpenAI, and the customer&rsquo;s test environment.', 9),
   ('Data-flow diagram and security answers', 'Partner architect', 'The diagram the customer&rsquo;s reviewer needs.', 'ok', 'Its own design freeze.', 5),
   ('Acceptance testing with adjusters', 'Partner test lead', 'A test report, and the load estimate.', 'gate', 'Evals at the agreed mark from OpenAI, and a pilot group from the customer.', 10),
   ('Rollout and training delivery', 'Partner change manager', 'Sessions run, attendance reported.', 'gate', 'The go decision, from the customer&rsquo;s sponsor.', 11),
   ('Handover', 'Partner engagement lead', 'A run-book the customer&rsquo;s platform owner accepts.', 'gate', 'Acceptance by the customer&rsquo;s claims platform owner.', 16)]),
]
cols = ''
n_streams = n_cross = 0
for name, sub, items in BOARD:
    rows = ''
    for n, owner, gives, kind, waits, wk in items:
        n_streams += 1
        n_cross += kind == 'gate'
        mark = '<span class="st gate">Waits on another team</span>' if kind == 'gate' else '<span class="st ok">Waits on nobody else</span>'
        rows += ('<div class="item"><b>%s</b><div class="own"><span class="role"><i>Owner:</i> %s</span><small>%s</small></div>'
                 '<div class="dep">%s<span class="wk">by week %d</span><small>%s</small></div></div>') % (n, owner, gives, mark, wk, waits)
    cols += '<div class="col"><h3>%s</h3><p>%s</p>%s</div>' % (name, sub, rows)
TALLY = ('<div class="tally own"><span><b>%d</b>workstreams</span><span><b>%d</b>with exactly one owner</span><span><b>3</b>teams</span></div>' % (n_streams, n_streams)
         + '<div class="tally dep"><span><b>%d</b>wait on another team</span><span><b>%d</b>wait on nobody else</span></div>' % (n_cross, n_streams - n_cross))

def lane(label, cls, start, end, text):
    return '<div class="lane"><b>%s</b><div class="bar %s" style="grid-column:%d/%d">%s</div></div>' % (label, cls, start + 1, end + 2, text)
GANTT = ('<div class="gantt g16" role="img" aria-label="Sixteen-week timeline in five phases: weeks 1 to 2, 3 to 8, 7 to 10, 11 to 12 and 13 to 16."><div class="gin">'
         '<div class="wkrow"><span>Week</span>' + ''.join('<span>%d</span>' % i for i in range(1, 17)) + '</div>'
         + lane('Scope, owners, baseline', 'a', 1, 2, 'Scope')
         + lane('Build and review', 'c', 3, 8, 'Agent, evals, integration, security review')
         + lane('Launch readiness', 'e', 7, 10, 'Capacity, testing, training')
         + lane('Launch', 'b', 11, 12, 'Pilot, then wider')
         + lane('First adoption', 'a', 13, 16, 'Adoption review, playbook')
         + '<div class="gates"><b>Gates</b><span style="grid-column:3/9">End of week 2: scope and baseline signed</span><span style="grid-column:9/11">End of week 8: evals pass, review closed</span><span style="grid-column:11/15">End of week 10: go or no-go</span><span style="grid-column:15/18">Week 14: first adoption review</span></div>'
         '</div></div>')

def phase(when, title, why, items, know):
    lis = ''
    for t, d, tags in items:
        lis += '<li><b>%s</b><span>%s</span>%s</li>' % (t, d, ''.join('<span class="tag">%s</span>' % x for x in tags))
    return '<div class="phase"><span class="when">%s</span><h3>%s</h3><p class="note" style="margin-top:8px">%s</p><ul>%s</ul><p class="know"><b>How I will know.</b> %s</p></div>' % (when, title, why, lis, know)

C, O, P = 'Customer', 'OpenAI', 'Partner'
PHASES = '<div class="phases">' + phase('Weeks 1 to 2', 'Scope, owners, baseline',
    'OpenAI&rsquo;s own sequence for managed deployments starts with outcomes and success criteria. So does this.', [
    ('Interview every workstream lead before the plan is written.', 'It is how I start a program. The answers become one script that all three teams plan from.', [C, O, P]),
    ('Agree the outcome and how it will be measured.', 'With the sponsor and the account team: the result to improve, the measure, and who reports it.', [C, O]),
    ('Set the baseline.', 'From the customer&rsquo;s own claims reports, and a first survey started by their admin. OpenAI&rsquo;s scheduled surveys begin at day 120, which is too late to be a baseline.', [C]),
    ('Name one owner for every workstream.', 'Seventeen workstreams, each with one name beside it. A workstream with two owners has none.', [C, O, P])],
    'Every workstream has a named owner and a first milestone, and the sponsor has signed the measures.') + phase('Weeks 3 to 8', 'Build and review',
    'The build and the reviews run side by side, because the review is often the longer of the two.', [
    ('Security, privacy and legal review.', 'The reviewer gets OpenAI&rsquo;s Trust Portal documents and the partner&rsquo;s data-flow diagram in week 3, not week 7.', [C, P]),
    ('Identity before invitations.', 'Domain, single sign-on and directory sync first. That is the order OpenAI&rsquo;s quickstart gives.', [C, O]),
    ('The agent, with evals written with adjusters.', 'Forward Deployed Engineers build it. The pass mark is agreed before the first test run.', [O, C]),
    ('Integration with the claims system.', 'The partner connects the agent. The customer supplies a test environment and a change window.', [P, C])],
    'The evals reach the agreed mark on real example claims, and the security review has no open blocker.') + phase('Weeks 7 to 10', 'Launch readiness',
    'A go or no-go is only honest if every gate shows its evidence. A gate with nothing behind it shows a dash, never green.', [
    ('Check the model against the launch date.', 'OpenAI publishes retirement dates and gives generally available models at least six months&rsquo; notice. The plan records the date beside the launch date.', [O]),
    ('Size capacity from testing, then order it.', 'Reserved capacity is bought per model through sales. The load estimate comes from acceptance testing, not from a guess.', [O, P]),
    ('Acceptance testing with the pilot adjusters.', 'On real claims, in the test environment, with the people who will use it.', [P, C]),
    ('Training, floor support and the support path.', 'Who trains, who attends, and who a stuck adjuster calls in week one.', [C, P, O]),
    ('The go or no-go review.', 'Eight gates, each with its evidence, and each owner in the room.', [C, O, P])],
    'Every gate has evidence or a stated reason it does not, and the sponsor decides in one meeting.') + phase('Weeks 11 to 12', 'Launch',
    'A staged rollout: a pilot group first, then the rest of claims. OpenAI describes the same staging for its managed deployments.', [
    ('The pilot group goes live.', 'With a daily check in the first week: errors, hand-offs to a person, and what adjusters rewrote.', [C, O, P]),
    ('The wider rollout.', 'Only after the pilot&rsquo;s first-week review.', [C, P]),
    ('A launch report to both sponsors.', 'What shipped, what did not, and what is still open.', [O])],
    'Adjusters in the pilot use it on live claims, and no gate was waved through to get there.') + phase('Weeks 13 to 16', 'First adoption, and the playbook',
    'Launch starts the measurement. It does not end the plan.', [
    ('Adoption against the baseline.', 'Usage from the analytics API, the outcome from the claims system, and what people report. Each number carries its source and its date. OpenAI says workspace analytics can lag by up to 48 hours, so the review says so too.', [O, C]),
    ('What the result means for usage.', 'The account team hears whether the ramp is on its planned date, and why, at the review and not at quarter end.', [O]),
    ('The playbook page.', 'What I would reuse, what I would not, and feedback for product, written so the next delivery lead can start from it.', [O]),
    ('Close-out with both sponsors, and handover.', 'The partner hands the run-book to the customer&rsquo;s platform owner.', [C, O, P])],
    'The sponsor can say what changed against the week-one baseline, and the next deployment starts from this one&rsquo;s plan.') + '</div>'

INDEX = ('<div class="w hero"><h1>One delivery plan for one priority deployment.</h1>'
  '<p class="lead">OpenAI&rsquo;s posting for Applied AI Delivery Lead asks for an &ldquo;integrated delivery plan&rdquo;: scope, milestones, accountable owners, dependencies, resource needs and success measures across customer, OpenAI and partner teams. This is one, for a made-up customer. I built it in one day from OpenAI&rsquo;s public pages, with AI agents doing the reading.</p>'
  '<div class="bottom"><div><b>The bottom line</b><span>OpenAI already publishes most of what a delivery plan needs. It sits on five sites, and no public page joins it up for one deployment.</span></div>'
  '<div><b>So the plan is</b><span>One page per deployment. Every workstream has one owner, every dependency a date, every number a source.</span></div>'
  '<div><b>Done means</b><span>The customer&rsquo;s people are using it, measured against a baseline set in week one, and the review can show why.</span></div></div>'
  '<div class="next"><a class="btn" href="prototype.html">Try the prototype</a><a class="btn ghost" href="evidence.html">Read the evidence</a></div></div>'

  '<section class="w" id="owners"><div class="shead"><div><h2>One deployment, three teams</h2>'
  '<p>The deployment is a claims assistant at Fernhill Mutual, a made-up insurer. An agent built on the API drafts claim summaries and next steps inside the adjusters&rsquo; claims system, and the claims organization gets ChatGPT Enterprise. A delivery partner does the integration.</p></div>'
  '<div class="seg" role="group" aria-label="Board view"><button type="button" aria-pressed="true" data-view="own">Who owns it</button><button type="button" aria-pressed="false" data-view="dep">What it waits on</button></div></div>'
  '<div class="board b3" data-view="own" id="board">' + cols + '</div>' + TALLY +
  '<p class="note" style="margin-top:14px">Fernhill Mutual and its people are made up. The role names in the OpenAI column are ones OpenAI&rsquo;s public pages use. Which role owns which workstream is my proposal: I cannot see from outside how OpenAI assigns them. <a href="evidence.html">Sources are on the evidence page.</a></p></section>'

  '<section class="w" id="weeks"><div class="shead"><div><h2>The sixteen weeks</h2><p>Five phases that overlap. Sixteen weeks is my assumption, to make the plan concrete. Scoping sets the real length. OpenAI&rsquo;s forward-deployed team has written of one first deployment that took two months.</p></div></div>'
  + GANTT + PHASES + '</section>'

  '<section class="w"><div class="two"><div><h2>The delivery review I would run</h2><p class="lead">Every two weeks with the customer, every week inside. One page, in the same order each time.</p>'
  '<p class="note" style="margin-top:12px">The posting asks for reviews that &ldquo;drive decisions and action&rdquo;. So decisions come first, while the people who can make them are in the room.</p></div><ul class="plain">'
  '<li><b>1. Decisions needed today.</b><span>Each with the options, the owner, and what waits on it.</span></li>'
  '<li><b>2. Gates, with their evidence.</b><span>Passed, at risk, late, not due, or no data. Never green over a blank.</span></li>'
  '<li><b>3. Risks that moved.</b><span>Only the ones that changed, each with one owner and a date.</span></li>'
  '<li><b>4. Launch confidence, and what it rests on.</b><span>Derived from the gates by a stated rule, so anyone can see why.</span></li>'
  '<li><b>5. Adoption against the baseline.</b><span>After launch. Before launch this part is empty, and says so.</span></li>'
  '<li><b>6. What a moved date means for usage.</b><span>If launch slips, the ramp slips with it. The account team hears it here first.</span></li></ul></div></section>'

  '<section class="w"><div class="two"><div><h2>What I would cut</h2><ul class="plain">'
  '<li><b>A second use case.</b><span>The posting says priority initiatives. One deployment taken to adoption, before a second starts.</span></li>'
  '<li><b>A weekly status deck.</b><span>The board is the status. A deck is a second copy that goes stale by Friday.</span></li>'
  '<li><b>Reports built on dashboard exports.</b><span>OpenAI&rsquo;s own guide says not to build a lasting report on dashboard labels. The board reads the analytics API and the customer&rsquo;s system.</span></li>'
  '<li><b>Fine-tuning.</b><span>OpenAI&rsquo;s self-serve fine-tuning stops taking new jobs on January 6, 2027. Prompts, tools and evals first.</span></li></ul></div>'
  '<div><h2>What would change this plan</h2><ul class="plain">'
  '<li><b>If OpenAI already has a plan format,</b><span>I use it. This one shows how I think, not what I would impose.</span></li>'
  '<li><b>If the deployment is a managed voice or chat agent,</b><span>it follows OpenAI&rsquo;s published sequence for those, and the partner&rsquo;s share changes.</span></li>'
  '<li><b>If the customer already runs ChatGPT Enterprise,</b><span>the identity and workspace work drops out and the plan is shorter.</span></li>'
  '<li><b>If the account team&rsquo;s forecast hangs on one date,</b><span>that date becomes a gate with an owner.</span></li>'
  '<li><b>If a workstream lead tells me something this page missed,</b><span>it goes in. That is what the week-one interviews are for.</span></li></ul></div></div></section>'

  '<section class="w"><div class="two"><div><h2>How I would measure it</h2><p class="lead">Four measures, agreed in week one and reported at every review.</p>'
  '<p class="note" style="margin-top:12px">I can see no baseline for any of them from outside, and I have made none up. Setting them is week 1 work.</p></div>'
  '<ul class="plain"><li><b>The outcome the sponsor chose.</b><span>For this customer, time from first notice of a claim to first contact. From their system, not ours.</span></li>'
  '<li><b>Share of the pilot group using it each week.</b><span>Adoption, not seats handed out.</span></li>'
  '<li><b>Gates passed on their planned date.</b><span>The delivery measure. A launch that arrives by waving gates through has not arrived.</span></li>'
  '<li><b>Days from launch to the first review with real numbers.</b><span>How soon the customer can see value for themselves.</span></li></ul></div>'
  '<div class="next"><a class="btn" href="prototype.html">See the delivery health board</a><a class="btn ghost" href="how.html">How I built this with AI</a></div></section>')

BOARD_JS = ('<script>(function(){var b=document.getElementById("board"),bs=document.querySelectorAll(".seg button"),t=document.querySelectorAll(".tally");'
  'function set(v,anim){b.dataset.view=v;bs.forEach(function(x){x.setAttribute("aria-pressed",x.dataset.view===v)});'
  't.forEach(function(x){x.hidden=!x.classList.contains(v)});'
  'if(anim)b.querySelectorAll(".item").forEach(function(i){i.classList.remove("changed");void i.offsetWidth;i.classList.add("changed")})}'
  'bs.forEach(function(x){x.addEventListener("click",function(){set(x.dataset.view,true)})});set("own",false)})();</script>')

page('index.html', 'One delivery plan for one priority deployment · Richard J. Valeo',
     'An integrated delivery plan for OpenAI’s Applied AI Delivery Lead role, by Richard J. Valeo. Unofficial, built from public pages.', INDEX, BOARD_JS)

# ---------------------------------------------------------------- the evidence
NF = '<span class="note">Not found</span>'
RIV = [
 ('us', 'OpenAI', U_ROLLOUT, 'Eight-step guide, and a nine-item quickstart', 'In the value guide, not in the rollout guides', 'Usage, task insights, outcomes, surveys, an API', 'Forward Deployed Engineers; AI advisors', 'Public, 73 named', '6 months for generally available models', 'Reserved Tier; Scale Tier', '99.9% on Scale Tier'),
 ('', 'Anthropic', 'https://academy.claude.com/tutorials/claude-enterprise-administrator-guide', 'Four-phase admin guide with a checklist', NF, 'Dashboard and two analytics APIs', 'Applied AI engineers', 'Public directory', 'At least 60 days', 'Through sales; the older tier is closed to new buyers', NF),
 ('', 'Google', 'https://knowledge.workspace.google.com/admin/generative-ai/getting-the-most-from-generative-ai-in-your-organization', 'Three-phase guide with named roles, for Workspace', 'Yes, a baseline survey in phase 1', 'Gemini reports; a value tab', 'Cloud Consulting; engineers placed with integrators', 'Partner network; list not readable', '12 months of availability, or at least 45 days', 'Provisioned Throughput', '99.5% for the Gemini API'),
 ('', 'Microsoft', 'https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-enablement-resources', 'Five-step admin guide; a success kit', NF, 'Copilot Dashboard; usage report', 'Forward-deployed engineers; FastTrack', 'Public directories', '60 days; 30 for preview', 'Provisioned throughput units', '99.9% on the product page'),
 ('', 'Amazon Bedrock', 'https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-gen-ai-maturity-model/introduction.html', 'A maturity model; no rollout checklist found', NF, 'Usage telemetry; no per-user view found', 'Forward Deployed Engineering', 'Partner network; list not readable', '6 months, or 45 days', 'Provisioned Throughput', '99.9%'),
 ('', 'Cohere', 'https://cohere.com/private-deployments', NF, NF, NF, 'Forward-deployed engineers; architects', 'Partner page; no list seen', 'Policy with no period stated', NF, NF),
 ('', 'Mistral', 'https://mistral.ai/our-method/', NF, NF, 'Usage dashboard', 'A named deployment team', 'Partner page; no list seen', '6 months; 1 month for others', 'Dedicated capacity mentioned', NF),
]
rows = ''.join('<tr%s><td><b>%s</b></td>%s</tr>' % (' class="us"' if c else '', a(u, n), ''.join('<td>%s</td>' % x for x in cells)) for c, n, u, *cells in RIV)
EVID = ('<div class="w hero"><h1>The evidence.</h1><p class="lead">Everything on this site comes from pages any visitor can open, read on ' + READ + '. I created no account, submitted no form and tested no system.</p></div>'
  '<section class="w"><h2>Where OpenAI already leads</h2><ul class="plain">'
  '<li><b>A rollout guide that starts with owners.</b><span>Step 1 of the admin rollout guide assigns an owner to each part of the rollout before anything is configured. A separate quickstart gives a nine-item checklist. ' + a(U_ROLLOUT, 'Rollout guide') + ', ' + a(U_QUICK, 'Quickstart') + '</span></li>'
  '<li><b>A written method for measuring value, with rules for reading the numbers.</b><span>Agree the result with the business owner and record the baseline. A zero may be a reporting gap, a sample is not a total, and estimates stay labeled as estimates. ' + a(U_UI, 'Usage Insights') + '</span></li>'
  '<li><b>A published delivery sequence.</b><span>For managed deployments: outcomes and success criteria, integration, security review, acceptance testing, a staged rollout, then review. ' + a(U_PRES, 'Help Center') + '</span></li>'
  '<li><b>Forward-deployed engineering, explained in public.</b><span>The head of the team has written how it works: start with the outcome, then make success repeatable. The posting&rsquo;s last duty asks for the same thing. ' + a(U_FDE, 'October 22, 2026') + '</span></li>'
  '<li><b>Six months&rsquo; notice before a generally available model retires.</b><span>Longer than the 60 days Anthropic and Azure state, with the shutdown date readable from the models endpoint. ' + a(U_DEP, 'Deprecations') + '</span></li>'
  '<li><b>A partner network with a public list.</b><span>73 partners named on the page, three tiers, and a pilot that aligns partner staff with OpenAI&rsquo;s own forward-deployed teams. ' + a(U_PN, 'Partner Network') + '</span></li>'
  '<li><b>Uptime in public.</b><span>The status page shows uptime per component: 99.97% for the APIs from August to November 2026. ' + a(U_STATUS, 'Status') + '</span></li></ul></section>'
  '<section class="w"><div class="shead"><div><h2>OpenAI beside six other providers</h2><p>What a customer&rsquo;s delivery lead can establish from each provider&rsquo;s own public pages. Each name links to the page that provider&rsquo;s row starts from.</p></div></div>'
  '<div class="tw"><table><thead><tr><th>Provider</th><th>Rollout guide</th><th>Baseline step</th><th>Adoption analytics</th><th>Delivery people</th><th>Partner list</th><th>Retirement notice</th><th>Reserved capacity</th><th>Public uptime figure</th></tr></thead><tbody>' + rows + '</tbody></table></div>'
  '<p class="note" style="margin-top:14px">&ldquo;Not found&rdquo; means not found on public pages, not that the provider lacks it. An AI research agent gathered the rival rows from each provider&rsquo;s own pages. I checked the OpenAI row against saved page text. Eight rival facts were spot-checked. The rest were not checked line by line, and Cohere and Mistral got a short look only.</p></section>'
  '<section class="w"><div class="two"><div><h2>What a delivery lead should know about this market</h2><p class="lead">Four things that shape a plan, whichever provider it is built on.</p></div><ul class="plain">'
  '<li><b>Every large provider now names forward-deployed engineers.</b><span>OpenAI, Google, Microsoft and Amazon all describe them on public pages, and Anthropic funds training for them. The engineers are no longer the difference. How their work is planned and joined to the customer&rsquo;s is.</span></li>'
  '<li><b>The model can retire during the program.</b><span>For generally available models, stated notice runs from 45 days to six months across the providers I read. A launch date and a retirement date belong on the same page.</span></li>'
  '<li><b>Measurement has moved from seats to outcomes.</b><span>OpenAI, Google and Microsoft all publish ways to connect usage to results. Of the rollout guides I read, only Google&rsquo;s makes a baseline survey a named step.</span></li>'
  '<li><b>Capacity is bought ahead.</b><span>OpenAI, Google, Microsoft and Amazon all document reserved capacity per model. It has to be sized before launch, from a test and not a guess.</span></li></ul></div></section>'
  '<section class="w"><div class="two"><div><h2>What is not on this page</h2></div><div><p>While reading, I found seven places where OpenAI&rsquo;s public pages disagree with each other, and a few smaller inconsistencies. Most touch things a customer plans around: capacity, retirement dates and reporting.</p>'
  '<p>Those are in a findings report I will send to OpenAI directly. A public page is the wrong place for them.</p>'
  '<div class="next"><a class="btn" href="index.html">Back to the plan</a><a class="btn ghost" href="how.html">How the research was run</a></div></div></div></section>')
page('evidence.html', 'The evidence · Richard J. Valeo', 'OpenAI’s public support for a customer’s delivery lead beside six other providers, with sources.', EVID)

# ---------------------------------------------------------------- how
def step(who, cls, title, text): return '<div class="step"><span class="who %s">%s</span><b>%s</b><span>%s</span></div>' % (cls, who, title, text)
HOW = ('<div class="w hero"><h1>How I built this.</h1><p class="lead">AI agents did the research and built these pages. Here is how the work was run, what was checked, and where the AI was wrong.</p></div>'
  '<section class="w"><h2>The workflow</h2><div class="flow">'
  + step('Me', 'me', 'Set the brief', 'Pitch the role with a plan and a working prototype. Read the company as its customer would first. Report what turns up, privately.')
  + step('AI', 'ai', 'Read everything public', 'The lead agent read OpenAI: 111 pages saved, two documentation indexes and 201 changelog entries searched. A second agent read six rival providers: 99 pages.')
  + step('AI', 'ai', 'Check each finding', 'Every OpenAI finding was checked against the saved page text. One was rewritten and one was dropped.')
  + step('AI', 'ai', 'Build', 'The plan, the delivery health board and a private findings report.')
  + step('Me', 'me', 'Read and stand behind it', 'I read every page of this site before sending it.')
  + '</div><p class="note" style="margin-top:16px">The lead agent was Claude. It did the OpenAI research, ran the rival research agent, did the checking and wrote the pages. One working day, ' + READ + '.</p></section>'
  '<section class="w"><div class="two"><div><h2>The rules the agents worked under</h2><ul class="plain">'
  '<li><b>Every claim carries its source.</b><span>A page address and where on the page. The page text is saved, so any claim can be checked again.</span></li>'
  '<li><b>&ldquo;Not found&rdquo; is never rewritten as &ldquo;missing&rdquo;.</b><span>The agents had to say where they looked. Only a statement by OpenAI itself counts as confirmed absent.</span></li>'
  '<li><b>Read only.</b><span>No account, no login, no form, no testing of any system. Nothing behind a sign-in was opened.</span></li>'
  '<li><b>A separate agent for rivals.</b><span>So what one provider says about another never stood in for that provider&rsquo;s own page.</span></li></ul></div>'
  '<div><h2>Where the AI was wrong or thin</h2><ul class="plain">'
  '<li><b>One finding was wrong on first read.</b><span>The agent wrote that OpenAI&rsquo;s newer capacity product states no service level. Its own page says the service level of the tier in use applies. The finding was rewritten.</span></li>'
  '<li><b>A search summary passed on a forum member&rsquo;s claim as fact.</b><span>It said one capacity product had been renamed to another. OpenAI&rsquo;s pages show two products. Dropped.</span></li>'
  '<li><b>The agent&rsquo;s own memory of OpenAI was out of date.</b><span>Model names, tiers and whole products had changed since its training. Nothing here comes from memory. Every statement comes from a page saved on ' + READ + '.</span></li>'
  '<li><b>The rival rows are thinner than the OpenAI row.</b><span>Eight rival facts were spot-checked. Several rival trust portals and partner lists could not be read at all, and the evidence page says so.</span></li>'
  '<li><b>The prototype&rsquo;s numbers are samples.</b><span>The only real facts on the board are the ones marked as OpenAI public pages, each with a link.</span></li></ul></div></div></section>'
  '<section class="w"><div class="two"><div><h2>Where my judgment came in</h2><p class="lead">The agents did the reading, the checking and the building. These five calls were mine.</p></div><ul class="plain">'
  '<li><b>Pitch the role with a plan and a working prototype.</b><span>The posting asks for a delivery plan and a clear view of delivery health. So I made both, not a letter about them.</span></li>'
  '<li><b>Read the company as its customer would, before pitching anything.</b><span>A delivery lead&rsquo;s first job is to see the deployment from the customer&rsquo;s chair.</span></li>'
  '<li><b>Report what turned up, privately.</b><span>If I find holes, I bring them up. The findings went into a report for OpenAI, not onto this site.</span></li>'
  '<li><b>Say what I cannot see.</b><span>I have no view inside OpenAI. The plan says which parts are my proposal and what would change it.</span></li>'
  '<li><b>Stand behind the output.</b><span>I read every page of this site before sending it. If something here is wrong, that is mine, not the agent&rsquo;s.</span></li></ul></div>'
  '<div class="next"><a class="btn" href="why.html">Why me</a><a class="btn ghost" href="index.html">Back to the plan</a></div></section>')
page('how.html', 'How I built this · Richard J. Valeo', 'The AI workflow behind this plan, what was checked, and where judgment came in.', HOW)

# ---------------------------------------------------------------- why me
def row(ask, have): return '<tr><td><b>%s</b></td><td>%s</td></tr>' % (ask, have)
PI = 'https://rjvaleo.github.io/case-pi-dashboard.html'
WHY = ('<div class="w hero"><h1>Why me.</h1><p class="lead">I run delivery for ten vendor teams on a program with contracted scope and a launch date that does not move. I built the board those teams plan from. This role is the same job from the other side of the table.</p></div>'
  '<section class="w"><h2>What the posting asks, and what I have done</h2><div class="tw"><table><thead><tr><th style="width:32%">The posting asks for</th><th>What I have done</th></tr></thead><tbody>'
  + row('Complex enterprise deployments with multiple teams and partners', 'Release Train Engineer on a tolling modernization program: ten workstreams, each with its own vendor or contractor team, onshore, offshore and in Europe, across five ten-week increments. Before that, two streaming apps on five platforms at A+E Networks, and about ten teams in India and California at Eptura. ' + a(PI, 'Case study'))
  + row('Scope through launch, with accountability for commitments', 'The first increment closed with every committed requirement accepted, and I ran the two-day close-out roadshow for the client. At a publicly traded retailer I ran readiness checkpoints and go or no-go decisions under SOX, and the go-live landed on time. At Meta I supported the embedded voice in the Ray-Ban Stories glasses and ran final QA. It shipped on the public launch date.')
  + row('Plans with milestones, owners, dependencies and success measures', 'I interviewed every workstream lead before planning and turned the answers into one script that every lead plans from. The planning board shows what each increment holds, what it inherits and what it hands on. Every metric is declared with the query that will produce it.')
  + row('A clear view of delivery health', 'The board never shows a number it cannot source, and a gate with no data shows a dash, never green. The prototype on this site carries the same two rules. ' + a('prototype.html', 'Prototype'))
  + row('Technical fluency with AI systems, APIs and security dependencies', 'Delivery lead at a stealth AI startup for teams fine-tuning Gemini, ChatGPT and Claude models on customer data. I co-built the requirements app my current program works in, including its role-based access, and it fails closed without a key. I also run local models on real coding jobs against hidden tests. ' + a('https://rjvaleo.github.io/case-rtm-tool.html', 'Case study'))
  + row('Judgment under ambiguity; finding material risks early', 'On my board, ambiguity is shown and never guessed, and machine suggestions stay marked as proposals until a person confirms them. I check the agents&rsquo; numbers: a reported 682 tests turned out to be 384.')
  + row('Trust with customers and executives, across teams outside my reporting line', 'Each of the ten teams belongs to its own vendor or contractor. I lead them through the plan and the Scrum of Scrums I rebuilt, and I run a retrospective with all leads at the end of each increment. Earlier, eight years on agency accounts for American Express, Citi and Toyota, from pitch to launch.')
  + row('Repeatable delivery methods', 'One planning script for ten vendors. Reusable AI skills that produce a meeting readout from a transcript and refresh the delivery report numbers from exports. The first increment&rsquo;s delivery report came from the board.')
  + '</tbody></table></div></section>'
  '<section class="w"><div class="two"><div><h2>The gap, plainly</h2></div><div><p class="lead">I have led delivery from the client and vendor-coordination side, not from inside a model provider. And I have never been accountable for a consumption or revenue number.</p>'
  '<p>The nearest I have come to the commercial side is agency work: estimates, statements of work, staffing plans and change orders. That is pricing a project, not owning a forecast. I would learn the second from the account teams, and I would not pretend to it in a review.</p>'
  '<p>My titles have been Scrum Master, Agile Coach and Release Train Engineer. What I bring is the plan, the gates and the honest board, and a habit of reading everything first. This site is that habit, done in a day.</p>'
  '<div class="next"><a class="btn" href="https://rjvaleo.github.io/">See my work</a><a class="btn ghost" href="https://www.linkedin.com/in/rjvaleo">LinkedIn</a></div></div></div></section>')
page('why.html', 'Why me · Richard J. Valeo', 'Richard J. Valeo’s record against OpenAI’s Applied AI Delivery Lead role.', WHY)

# ---------------------------------------------------------------- prototype (markup here, behaviour in assets/proto.js)
PROTO = open(os.path.join(HERE, '_proto.html'), encoding='utf-8').read()
page('prototype.html', 'Delivery health board prototype · Richard J. Valeo', 'A clickable prototype of a delivery health board for one AI deployment. Sample data, made-up customer.', PROTO, '<script src="assets/proto.js"></script>')
