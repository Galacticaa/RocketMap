COMMON_POKEMON = [16, 19, 23, 27, 29, 32, 41, 43, 46, 52, 54, 60, 69,
                  72, 74, 77, 81, 98, 118, 120, 129, 161, 165, 167,
                  177, 183, 187, 191, 194, 198, 209, 218]


def contains_rares(map_cells):
    for cell in map_cells:
        for p in cell.wild_pokemons:
            if p.pokemon_data.pokemon_id not in COMMON_POKEMON:
                return True

        for p in cell.nearby_pokemons:
            if p.pokemon_id not in COMMON_POKEMON:
                return True

    return False


def format_rareless_scans(account):
    total = account.get('rareless_scans', None)
    if (total is None):
        blinded = ''
    elif total < 5:
        blinded = 'No'
    else:
        blinded = 'Maybe' if total < 20 else 'Yes'

    if blinded:
        blinded = '{} ({})'.format(blinded, total if total <= 50 else '50+')

    return blinded



def update_rareless_scans(cells, account, log):
    if contains_rares(cells):
        if account['rareless_scans'] > 0:
            log.debug('Account {} is no longer shadow banned!'.format(account['username']))
        account['rareless_scans'] = 0
    else:
        log.debug('Rareless scan on account {}. Bumping counter.'.format(account['username']))
        account['rareless_scans'] += 1

        if 20 < account['rareless_scans']:
            log.warning('Account {} has had {} consecutive rareless ' \
                        'scans. It is most likely blind.'.
                        format(account['username'],
                               account['rareless_scans']))
