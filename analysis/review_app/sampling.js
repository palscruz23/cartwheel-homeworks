/* Saved sample membership stays unchanged; dimensions only filter the queue. */
function dimensionValues(traces, dimension) {
  return [...new Set(traces.map(trace => trace.dimensions?.[dimension]).filter(value => value !== undefined))].sort();
}

function sampleMatches(manifest, traces, methods, dimensions) {
  const matches = new Set((manifest.picks || []).filter(pick => {
    const reason = String(pick.reason || pick.strategy || manifest.strategy || '').toLowerCase();
    return (methods.includes('uniform') && /random|uniform/.test(reason)) ||
      (methods.includes('clustered') && /cluster/.test(reason));
  }).map(pick => pick.trace_id));
  const filters = Object.entries(dimensions);
  for (const trace of traces) {
    if (filters.length && filters.every(([name, values]) => {
      const value = trace.dimensions?.[name];
      return value !== undefined && (!values.length || values.includes(value));
    })) matches.add(trace.id);
  }
  return matches;
}

function conversationMatchesSearch(session, query) {
  const term = query.trim().toLowerCase();
  return !term || [session.id, ...session.traces.flatMap(trace => [trace.id, trace.scenario])]
    .some(value => String(value ?? '').toLowerCase().includes(term));
}

function commentCountsByTrace(annotations, source) {
  const counts = new Map();
  for (const note of annotations) {
    const origin = note.source ?? note.author ?? 'human';
    if (source && origin !== source) continue;
    counts.set(note.trace_id, (counts.get(note.trace_id) || 0) + 1);
  }
  return counts;
}

function conversationsWithComments(sessions, counts) {
  return sessions.filter(session => session.traces.some(trace => counts.has(trace.id)));
}

if (typeof module !== 'undefined') module.exports = {dimensionValues, sampleMatches, conversationMatchesSearch, commentCountsByTrace, conversationsWithComments};
