import { useEffect, useState } from 'react'
import { Mention, MentionsInput } from 'react-mentions'

import defaultMentionStyle from './defaultMentionStyle'
import defaultStyle from './defaultStyle'

import styled from 'styled-components'
import { useAssignedUserListService } from 'services'

import Typography from '@l3-lib/ui-core/dist/Typography'
import Avatar from '@l3-lib/ui-core/dist/Avatar'

import l3Icon from 'assets/avatars/l3.png'
import { useAgentsService } from 'services/agent/useAgentsService'
import { useTeamOfAgentsService } from 'services/team/useTeamOfAgentsService'

type OnChangeHandlerType = (event: { target: { value: string } }) => void

type MentionsProps = {
  inputRef: React.RefObject<HTMLTextAreaElement> | null
  value: string
  onChange: OnChangeHandlerType
  onKeyDown: React.KeyboardEventHandler<HTMLInputElement | HTMLTextAreaElement>
  setValue: any
  isGeneralChat: boolean
}

const Mentions = ({
  inputRef,
  onChange,
  onKeyDown,
  value,
  setValue,
  isGeneralChat,
}: MentionsProps) => {
  const [focusAfterAdd, setFocusAfterAdd] = useState(false)

  const { data: users } = useAssignedUserListService()

  const { data: agents } = useAgentsService()
  const { data: teamOfAgents } = useTeamOfAgentsService()

  const agentMentions = agents.map((agent: any) => {
    const { id, name } = agent.agent

    return {
      display: name,
      id: `agent__${id}`,
      type: 'Agent',
      icon: <Avatar size={Avatar.sizes.SMALL} src={l3Icon} type={Avatar.types.IMG} rectangle />,
    }
  })

  const teamOfAgentsMentions = teamOfAgents.map((team: any) => {
    const { id, name } = team

    return {
      display: name,
      id: `team__${id}`,
      type: 'Team Of Agents',
      icon: <Avatar size={Avatar.sizes.SMALL} src={l3Icon} type={Avatar.types.IMG} rectangle />,
    }
  })

  const usersMentions: any = users.map((user: any) => {
    return {
      display: user.assigned_user_first_name,
      id: `user__${user.assigned_user_id}`,
      type: 'Team Member',
    }
  })

  const mentions = isGeneralChat
    ? [...agentMentions, ...teamOfAgentsMentions, ...usersMentions]
    : usersMentions

  const displayTransform = (id: string) => {
    const display = mentions.find((item: any) => item.id.includes(id))?.display
    // Add the "@" symbol to the display when the suggestion is picked
    return `@${display} `
  }

  useEffect(() => {
    if (focusAfterAdd) {
      inputRef?.current?.setSelectionRange(value.length, value.length)
    }

    return () => {
      setFocusAfterAdd(false)
    }
  }, [focusAfterAdd])

  return (
    <>
      <StepWrapper>
        <div className='direction-input-wrapper'>
          <StyledMentionsInput
            style={defaultStyle}
            className='direction-input'
            // forceSuggestionsAboveCursor
            inputRef={inputRef}
            onKeyDown={onKeyDown}
            value={value}
            onChange={onChange}
            customSuggestionsContainer={children => <StyledContainer>{children}</StyledContainer>}
          >
            <Mention
              onAdd={() => {
                setValue((prevState: string) => {
                  return `${prevState} `
                })
                setFocusAfterAdd(true)
              }}
              renderSuggestion={suggestion => {
                const { type, icon }: any = suggestion
                return (
                  <StyledSuggestionsWrapper>
                    <StyledNameWrapper>
                      {icon}
                      <div>{suggestion.display}</div>
                    </StyledNameWrapper>

                    <Typography
                      value={type}
                      type={Typography.types.LABEL}
                      size={Typography.sizes.xss}
                      customColor={'rgba(255, 255, 255, 0.4)'}
                    />
                  </StyledSuggestionsWrapper>
                )
              }}
              style={defaultMentionStyle}
              displayTransform={displayTransform}
              data={mentions}
              trigger={'@'}
              markup='@[__display__](__id__)__mention__'
            />
          </StyledMentionsInput>
        </div>
      </StepWrapper>
    </>
  )
}

export default Mentions

const StyledMentionsInput = styled(MentionsInput)`
  width: 100%;
`
const StepWrapper = styled.div`
  .direction-input-wrapper {
    border: none;

    textarea {
      &:focus {
        outline: none;
        box-shadow: none;
      }
    }
  }

  .mention-suggestion {
    width: 100%;
  }
`

const StyledContainer = styled.div`
  background: var(--gradient-blue, linear-gradient(180deg, #3582ca 0%, #405fc2 100%));

  width: 100%;

  position: fixed;
  bottom: 55px;
  left: 50%;
  transform: translateX(-50%);

  border-radius: 8px;
  padding: 10px 0;
  backdrop-filter: blur(100px);
  -webkit-backdrop-filter: blur(100px);
`
const StyledSuggestionsWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
`
const StyledNameWrapper = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
`
