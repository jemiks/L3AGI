import { FormikProvider } from 'formik'

import styled from 'styled-components'
import Heading from '@l3-lib/ui-core/dist/Heading'

import useLogin from 'pages/Auth/Login/useLogin'
import useGithubLogin from 'pages/Auth/Login/useGithubLogin'
import TextFieldFormik from 'components/TextFieldFormik'
import { StyledCenterFormContainer, StyledFormContainer } from 'styles/globalStyle.css'

import Typography from '@l3-lib/ui-core/dist/Typography'
import Button from '@l3-lib/ui-core/dist/Button'

import githubIcon from 'assets/icons/githubIcon.png'

import './login.css'
import { useModal } from 'hooks'
import {
  StyledImageWrapper,
  StyledImg,
  StyledInnerButtonWrapper,
} from 'components/HeaderButtons/HeaderButtons'
import OrDivider from 'components/OrDivider/OrDivider'

const ErrorResendVerification = ({ resendVerifyEmail }: any) => (
  <p className='mb-0'>
    Please verify your email, didn’t receive verification email link?
    <StyledNavLink onClick={() => resendVerifyEmail()} className='text-secondary d-inline-block'>
      <u> Resend</u>
    </StyledNavLink>
  </p>
)

const Login = () => {
  const { formik, alertMessage, showResendAlert, resendVerifyEmailHandle } = useLogin()
  const { githubLogin } = useGithubLogin()
  const { openModal } = useModal()

  return (
    <StyledCenterFormContainer>
      {alertMessage.message && alertMessage.type && <span>{alertMessage.message}</span>}

      {showResendAlert && <ErrorResendVerification resendVerifyEmail={resendVerifyEmailHandle} />}

      <StyledHeaderWrapper>
        <Heading
          value={'Complete your mission'}
          type={Heading.types.h2}
          customColor='rgba(255, 255, 255, 0.9)'
          style={{ fontSize: 24, lineHeight: 'normal' }}
        />
        <Typography
          value={`AI agents' team collaboration as effective as human collaboration.`}
          type={Typography.types.label}
          size={Typography.sizes.sm}
          customColor={'rgba(255,255,255, 0.6)'}
        />
      </StyledHeaderWrapper>

      <StyledFormContainer>
        {/* <StyledColumnContainer>
          <Checkbox
            size='small'
            kind='secondary'
            label='You will keep this between us 😉'
            labelClassName='checkbox_label'
          />
        </StyledColumnContainer> */}
        {/* <Typography
          value='Forget password?'
          type={Typography.types.label}
          size={Typography.sizes.lg}
          as={'a'}
          customColor='#FFFFFF'
          style={{
            textDecorationLine: 'underline',
            cursor: 'pointer',
            textAlign: 'center',
            textUnderlineOffset: 5,
            marginTop: 18,
          }}
        /> */}
        <Button
          onClick={async () => {
            const res = await githubLogin()
            window.location.href = res.auth_url
          }}
        >
          <StyledInnerButtonWrapper>
            <StyledImageWrapper secondary>
              <StyledImg src={githubIcon} />
            </StyledImageWrapper>
            Login with Github
          </StyledInnerButtonWrapper>
        </Button>

        <OrDivider />

        <FormikProvider value={formik}>
          <StyledInputWrapper>
            <TextFieldFormik
              label='Email'
              field_name='email'
              placeholder='Enter email...'
              size='small'
            />
            <TextFieldFormik
              label='Password'
              field_name='password'
              placeholder='Enter password...'
              type='password'
              size='small'
            />
          </StyledInputWrapper>
        </FormikProvider>

        <Button onClick={() => formik.handleSubmit()} size={Button.sizes.MEDIUM}>
          Start
        </Button>

        <StyledSignUpWrapper>
          <Typography
            value={`Don't have an account?`}
            type={Typography.types.label}
            size={Typography.sizes.md}
            customColor={'rgba(255,255,255, 0.6)'}
          />
          <button
            onClick={() => {
              openModal({ name: 'login-modal', data: { isRegister: true } })
            }}
          >
            <Typography
              value='Sign up'
              type={Typography.types.label}
              size={Typography.sizes.md}
              as={'a'}
              customColor='#FFFFFF'
              style={{
                textDecorationLine: 'underline',
                cursor: 'pointer',
                textAlign: 'center',
                textUnderlineOffset: 5,
                marginTop: 18,
              }}
            />
          </button>
        </StyledSignUpWrapper>
      </StyledFormContainer>
    </StyledCenterFormContainer>
  )
}

export default Login

const StyledNavLink = styled.a`
  color: #19b3ff;
  cursor: pointer;
`
const StyledSignUpWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
`

export const StyledInputWrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
`
export const StyledHeaderWrapper = styled.div`
  display: flex;
  flex-direction: column;
  padding: 0 87px;
  align-items: center;
  text-align: center;
  gap: 22px;

  margin-top: 10px;
`
