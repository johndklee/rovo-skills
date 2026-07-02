import api, { route } from '@forge/api';

interface GetSprintIssuesPayload {
  projectKey: string;
}

interface SprintIssue {
  key: string;
  summary: string;
  status: string;
  assignee: string;
  type: string;
}

interface PublishSprintReportPayload {
  spaceKey: string;
  title: string;
  content: string;
}

export async function getSprintIssues(payload: GetSprintIssuesPayload): Promise<SprintIssue[]> {
  const { projectKey } = payload;
  const jql = `project = "${projectKey}" AND sprint in openSprints() ORDER BY status ASC`;

  const response = await api.asApp().requestJira(route`/rest/api/3/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jql,
      fields: ['summary', 'status', 'assignee', 'issuetype'],
      maxResults: 100,
    }),
  });

  if (!response.ok) {
    throw new Error(`Jira search failed: ${response.status} ${await response.text()}`);
  }

  const data = await response.json();
  return data.issues.map((issue: any) => ({
    key: issue.key,
    summary: issue.fields.summary,
    status: issue.fields.status?.name ?? 'Unknown',
    assignee: issue.fields.assignee?.displayName ?? 'Unassigned',
    type: issue.fields.issuetype?.name ?? 'Unknown',
  }));
}

export async function publishSprintReport(payload: PublishSprintReportPayload) {
  const { spaceKey, title, content } = payload;

  const spaceResponse = await api
    .asApp()
    .requestConfluence(route`/wiki/api/v2/spaces?keys=${spaceKey}`);
  if (!spaceResponse.ok) {
    throw new Error(`Confluence space lookup failed: ${spaceResponse.status}`);
  }
  const spaceData = await spaceResponse.json();
  const space = spaceData.results?.[0];
  if (!space) {
    throw new Error(`No Confluence space found for key "${spaceKey}"`);
  }

  const pageResponse = await api.asApp().requestConfluence(route`/wiki/api/v2/pages`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      spaceId: space.id,
      status: 'current',
      title,
      body: {
        representation: 'storage',
        value: content,
      },
    }),
  });

  if (!pageResponse.ok) {
    throw new Error(
      `Confluence page creation failed: ${pageResponse.status} ${await pageResponse.text()}`
    );
  }

  return pageResponse.json();
}
