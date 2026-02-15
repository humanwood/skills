# Clawauth Commands (Agent Reference)

## Get command access

```bash
npx clawauth --help
```

```bash
npm i -g clawauth
clawauth --help
```

## Discover providers

```bash
clawauth providers --json
```

## Start async auth

```bash
clawauth login start <provider> --json
```

Key fields from output:

- `sessionId`
- `shortAuthUrl`
- `expiresIn`
- `statusCommand`
- `claimCommand`

## Check status later

```bash
clawauth login status <sessionId> --json
```

Status values:

- `pending`
- `completed`
- `error`

## Claim completed session

```bash
clawauth login claim <sessionId> --json
```

On `completed`, output includes token payload and keychain storage metadata.

## Optional blocking mode

```bash
clawauth login wait <sessionId> --json
```

## Recover lost context

```bash
clawauth sessions --json
```

```bash
clawauth session-rm <sessionId> --json
```

## Token retrieval

```bash
clawauth token list --json
```

```bash
clawauth token get <provider> --json
```

```bash
clawauth token env <provider>
```

## Detailed manual

```bash
clawauth explain
```
