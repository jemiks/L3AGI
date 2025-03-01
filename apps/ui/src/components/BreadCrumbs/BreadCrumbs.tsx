import { NavLink, useParams } from 'react-router-dom'

import styled from 'styled-components'
import useBreadcrumbs from 'use-react-router-breadcrumbs'

import Typography from '@l3-lib/ui-core/dist/Typography'
import Button from '@l3-lib/ui-core/dist/Button'
import { useAgentByIdService } from 'services/agent/useAgentByIdService'
import { useDatasourceByIdService } from 'services/datasource/useDatasourceByIdService'
import { useToolsService } from 'services/tool/useToolsService'
import { useTeamOfAgentsByIdService } from 'services/team/useTeamOfAgentsByIdService'

const GetAgentName = () => {
  const params = useParams()
  const { agentId } = params

  const { data: agentById } = useAgentByIdService({ id: agentId || '' })

  return <span>{agentById?.agent?.name}</span>
}

const GetDatasourceName = () => {
  const params = useParams()
  const { datasourceId } = params

  const { data: datasourceById } = useDatasourceByIdService({ id: datasourceId || '' })

  return <span>{datasourceById?.name}</span>
}

const GetToolkitName = () => {
  const params = useParams()
  const { toolkitId } = params

  const { data: toolsData } = useToolsService()
  const tool = toolsData?.filter((tool: any) => toolkitId === tool.toolkit_id)

  return <span>{tool[0]?.name}</span>
}

const GetTeamOfAgentsName = () => {
  const params = useParams()
  const { teamId } = params

  const { data: teamOfAgent } = useTeamOfAgentsByIdService({ id: teamId || '' })

  return <span>{teamOfAgent?.name}</span>
}

const routes: any = [
  { path: '/developers', breadcrumb: 'Developers' },
  { path: '/developers/logs', breadcrumb: 'Logs' },
  { path: '/developers/webhook', breadcrumb: 'Webhook' },

  // account
  { path: '/account', breadcrumb: 'Profile' },

  { path: '/agents/:agentId', breadcrumb: GetAgentName },
  { path: '/agents/create-agent', breadcrumb: 'Create Agent' },

  { path: '/datasources/:datasourceId', breadcrumb: GetDatasourceName },
  { path: '/datasources/create-datasource', breadcrumb: 'Add Datasource' },

  { path: '/toolkits/:toolkitId', breadcrumb: GetToolkitName },

  { path: '/team-of-agents/:teamId', breadcrumb: GetTeamOfAgentsName },

  //chat
  { path: '/copilot', breadcrumb: null },
  { path: '/chat', breadcrumb: null },
  { path: '/chat/history', breadcrumb: null },
  // { path: '/copilot/game', breadcrumb: null },
  // { path: '/copilot/collection', breadcrumb: null },
  // { path: '/copilot/game/:gameId', breadcrumb: GetGameName },
  // { path: '/copilot/collection/:collectionId', breadcrumb: GetCollectionName },
]

type BreadcrumbsProps = {
  onClick?: () => void
}

const Breadcrumbs = ({ onClick }: BreadcrumbsProps) => {
  const breadcrumbs = useBreadcrumbs(routes)

  return (
    <StyledBreadcrumbUl>
      {breadcrumbs.length > 0
        ? breadcrumbs.map(({ match, breadcrumb }) => {
            return (
              <StyledBreadcrumbLi key={match.pathname}>
                <StyledNavLink key={match.pathname} to={match.pathname} onClick={onClick}>
                  <Button size={Button.sizes.SMALL} kind={Button.kinds.TERTIARY}>
                    <Typography
                      value={breadcrumb}
                      type={Typography.types.LABEL}
                      size={Typography.sizes.sm}
                      customColor={'rgba(255, 255, 255, 0.80)'}
                    />
                  </Button>
                </StyledNavLink>
                <div className='line' />
              </StyledBreadcrumbLi>
            )
          })
        : breadcrumbs.map(({ match, breadcrumb }) => {
            return (
              <StyledBreadcrumbLi key={match.pathname}>
                <StyledNavLink key={match.pathname} to={match.pathname} onClick={onClick}>
                  <Button size={Button.sizes.SMALL} kind={Button.kinds.TERTIARY}>
                    <Typography
                      value={breadcrumb}
                      type={Typography.types.LABEL}
                      size={Typography.sizes.sm}
                      customColor={'rgba(255, 255, 255, 0.80)'}
                    />
                  </Button>
                </StyledNavLink>
              </StyledBreadcrumbLi>
            )
          })}

      {}
    </StyledBreadcrumbUl>
  )
}

export default Breadcrumbs

const StyledNavLink = styled(NavLink)`
  cursor: pointer;
  font-style: normal;
  font-weight: 500;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
`

const StyledBreadcrumbUl = styled.ul`
  list-style-type: none;
  padding: 0;
  display: flex;
  li:last-child {
    div {
      display: none;
    }
  }
`

const StyledBreadcrumbLi = styled.li`
  min-height: 34px;
  display: flex;
  align-items: center;
  a {
    padding: 0 15px;
  }
  .line {
    height: 50%;
    width: 1px;
    background: rgba(255, 255, 255, 0.1);
  }
`
